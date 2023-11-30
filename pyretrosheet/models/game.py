"""Encapsulates Retrosheet game data."""
from collections.abc import Iterator, Sequence
from dataclasses import dataclass

from pyretrosheet.models.exceptions import ParseError
from pyretrosheet.models.game_id import GameID
from pyretrosheet.models.play import Play
from pyretrosheet.models.player import Player

ChronologicalEvent = Player | Play
ChronologicalEvents = Sequence[ChronologicalEvent]


class GameIDNotFoundError(Exception):
    """Error when unable to find a game's id."""

    def __init__(self, first_game_line: str):
        """Initialize the exception.

        Args:
            first_game_line: the first line of game lines
        """
        super().__init__(f"Unable to find game id for game: {first_game_line=}")


@dataclass
class Game:
    """A game as defined in Retrosheet.

    Args:
        game_id: the game id
        info: miscellaneous encoded information like temperature, attendance, umpire names, etc.
        chronological_events: the chronological order of events occurring
        earned_runs: map of player id to earned runs
    """

    game_id: GameID
    info: dict[str, str]
    chronological_events: ChronologicalEvents
    earned_runs: dict[str, int]

    @classmethod
    def from_game_lines(cls, game_lines: list[str]) -> "Game":
        """Load a game from game lines.

        Args:
            game_lines: game lines from a game
        """
        game_id = None
        info = {}
        chronological_events: ChronologicalEvents = []
        earned_runs = {}
        for i, line in enumerate(game_lines):
            parts = line.split(",")
            try:
                match parts[0]:
                    case "id":
                        game_id = GameID.from_id_line(line)

                    case "info":
                        info[parts[1]] = parts[2]

                    case "start":
                        chronological_events.append(Player.from_start_or_sub_line(line, is_sub=False))

                    case "sub":
                        chronological_events.append(Player.from_start_or_sub_line(line, is_sub=True))

                    case "play":
                        comment_lines = list(_yield_comment_lines_following_play(i, game_lines))
                        chronological_events.append(Play.from_play_line(line, comment_lines))

                    case "data":
                        earned_runs[parts[2]] = int(parts[3])
            except ParseError as e:
                raise ParseError(e.looking_for_value, e.raw_value, line) from e

        if not game_id:
            raise GameIDNotFoundError(game_lines[0])

        return cls(
            game_id=game_id,
            info=info,
            chronological_events=chronological_events,
            earned_runs=earned_runs,
        )

    @property
    def home_team_id(self) -> str:
        """The id of the home team."""
        return self.info["hometeam"]

    @property
    def visiting_team_id(self) -> str:
        """The id of the visiting team."""
        return self.info["visteam"]


def _yield_comment_lines_following_play(play_line_number: int, game_lines: list[str]) -> Iterator[str]:
    """Yield all comment lines that follow a play line."""
    line_pointer = 1
    while True:
        line = game_lines[play_line_number + line_pointer]
        parts = line.split(",")
        if parts[0] == "com":
            yield line
            line_pointer += 1
        else:
            break
