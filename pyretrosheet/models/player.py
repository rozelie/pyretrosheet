"""Encapsulates Retrosheet player data."""
from dataclasses import dataclass


@dataclass
class Player:
    """A player as defined in Retrosheet.

    Args:
        id: the player's Retrosheet id
        name: the player's name
        team_id: the player's team's Retrosheet id
        batting_order_position: the player's batting order position
        fielding_position: the player's fielding position
        earned_runs: earned runs allowed from pitching, if any
        raw: str
    """

    id: str
    name: str
    team_id: str
    batting_order_position: int
    fielding_position: int
    raw: str

    @classmethod
    def from_retrosheet_start_or_sub_line(cls, start_or_sub_line: str) -> "Player":
        """Load a player from Retrosheet start or sub line.

        Args:
            start_or_sub_line: start or sub line from Retrosheet play-by-play data
        """
        raise NotImplementedError()
