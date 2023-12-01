"""Encapsulates a Retrosheet game id."""
import datetime as dt
from dataclasses import dataclass


@dataclass
class GameID:
    """A game ID as defined in Retrosheet.

    Example: id,ATL198304080
        - ATL home team
        - date of April 8th, 1983
        - first game of the day

    Args:
        home_team_id: the home team's id
        date: the date the game was played
        game_number: the number of the game happening on the date (single game (0), first game (1) or second game (2))
        raw: the raw value of the game id
    """

    home_team_id: str
    date: dt.date
    game_number: int
    raw: str

    @classmethod
    def from_id_line(cls, id_line: str) -> "GameID":
        """Load the GameID from a 'id' line.

        Args:
            id_line: the 'id' line
        """
        id_value = id_line.split(",")[1]
        return cls(
            home_team_id=id_value[:3],
            date=dt.date(year=int(id_value[3:7]), month=int(id_value[7:9]), day=int(id_value[9:11])),
            game_number=int(id_value[-1]),
            raw=id_line,
        )
