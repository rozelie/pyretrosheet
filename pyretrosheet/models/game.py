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
        id: the game's id
        info: miscellaneous encoded information like temperature, attendance, umpire names, etc.
        chronological_events: the chronological order of events occurring
        earned_runs: map of player id to earned runs
    """

    id: GameID
    info: dict[str, str]
    chronological_events: ChronologicalEvents
    earned_runs: dict[str, int]

    def __repr__(self) -> str:
        """Pretty representation of a game."""
        lines = [
            "Game(",
            f"  id={self.id},",
            f"  home_team_id={self.home_team_id},",
            f"  visiting_team_id={self.visiting_team_id},",
            f"  num_chronological_events={len(self.chronological_events)},",
            f"  earned_runs={self.earned_runs},",
            ")",
        ]
        return "\n".join(lines)

    @classmethod
    def from_game_lines(cls, game_lines: list[str], basic_info_only: bool = False) -> "Game":
        """Load a game from game lines.

        Args:
            game_lines: game lines from a game
            basic_info_only: only populate basic info (game id and participating teams)
        """
        id_ = None
        info = {}
        chronological_events: ChronologicalEvents = []
        earned_runs = {}
        for i, line in enumerate(game_lines):
            parts = line.split(",")
            try:
                match parts[0]:
                    case "id":
                        id_ = GameID.from_id_line(line)

                    case "info":
                        info[parts[1]] = parts[2]

                    case "start":
                        # start lines mark the end of the id and info lines needed for basic info
                        if basic_info_only:
                            break

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
            except Exception as e:
                raise ParseError("unknown", "unknown", line) from e

        if not id_:
            raise GameIDNotFoundError(game_lines[0])

        return cls(
            id=id_,
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

    @property
    def pretty_id(self) -> str:
        """Simple, human-readable identifier for the game."""
        return f"{self.id.date.strftime('%Y/%m/%d')} {self.visiting_team_id} @ {self.home_team_id}"


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
