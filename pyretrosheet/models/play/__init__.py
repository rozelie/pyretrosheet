"""Encapsulates Retrosheet play data."""
from dataclasses import dataclass

from pyretrosheet.models.play.event import Event
from pyretrosheet.models.team import TeamLocation


@dataclass
class Play:
    """A play as defined in Retrosheet.

    Args:
        inning: the inning the play occurred in
        team_location: the team's location
        batter_id: the player id of the batter
        count: the count on the batter
        pitches: all the pitches to the batter in the plate appearance
        comments: comments regarding the play, from 'com' lines in Retrosheet data
        event: the event describes the play that occurred
        raw: the raw play line
    """

    inning: int
    team_location: TeamLocation
    batter_id: str
    count: str
    pitches: str
    comments: list[str]
    event: Event
    raw: str

    @classmethod
    def from_play_line(cls, play_line: str, comment_lines: list[str] | None) -> "Play":
        """Load a play from a play line.

        Args:
            play_line: line for a play (format: play,inning,home/visitor,player id,count,pitches,event)
                Examples include: 'play,7,0,saboc001,01,CX,8/F78', 'play,1,0,marts002,22,CBCBX,S9/L89S-'
            comment_lines: comment lines that reference the play, if present
        """
        # Handle weird case of 'play,3,1,smitj106,??,,43,2-3' where I think this is an encoding error
        if play_line == "play,3,1,smitj106,??,,43,2-3":
            play_line = "play,3,1,smitj106,??,?,43.2-3"

        _, inning, team_location, batter_id, count, pitches, event = play_line.split(",")
        return cls(
            inning=int(inning),
            team_location=TeamLocation(int(team_location)),
            batter_id=batter_id,
            count=count,
            pitches=pitches,
            comments=[c.split(",")[1] for c in comment_lines or []],
            event=Event.from_play_event(event),
            raw=play_line,
        )
