"""Encapsulates Retrosheet player data."""
from dataclasses import dataclass

from pyretrosheet.models.team import TeamLocation


@dataclass
class Player:
    """A player as defined in Retrosheet.

    Args:
        id: the player's id
        name: the player's name
        team_location: the player's team's location
        batting_order_position: the player's batting order position
        fielding_position: the player's fielding position
        raw: str
    """

    id: str
    name: str
    team_location: TeamLocation
    batting_order_position: int
    fielding_position: int
    is_sub: bool
    raw: str

    @classmethod
    def from_start_or_sub_line(cls, start_or_sub_line: str, is_sub: bool) -> "Player":
        """Load a player from Retrosheet start or sub line.

        Args:
            start_or_sub_line: start or sub line from Retrosheet play-by-play data
                Examples include: 'start,richg001,"Gene Richards",0,1,7', 'sub,votha001,"Austin Voth",1,0,1'
            is_sub: whether the player is coming from a sub line or not
        """
        # handle rare cases where a comma is within a player's name
        for name, new_name in [
            ("George Watkins,", "George Watkins"),
            ("Clyde,Barfoot", "Clyde Barfoot"),
            ("Burgess,Smoky", "Burgess Smoky"),
            ("Richie Scheinblum,", "Richie Scheinblum"),
        ]:
            if name in start_or_sub_line:
                start_or_sub_line = start_or_sub_line.replace(name, new_name)

        _, player_id, name, team_location, batting_order_position, fielding_position = start_or_sub_line.split(",")
        return cls(
            id=player_id,
            name=name.replace('"', ""),
            team_location=TeamLocation(int(team_location)),
            batting_order_position=int(batting_order_position),
            fielding_position=int(fielding_position),
            is_sub=is_sub,
            raw=start_or_sub_line,
        )
