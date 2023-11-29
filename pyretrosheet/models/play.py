"""Encapsulates Retrosheet play data."""
import re
from dataclasses import dataclass

from pyretrosheet.models.base import Base
from pyretrosheet.models.team import TeamLocation


class ParseError(Exception):
    """Raise on Retrosheet data parsing errors."""

    def __init__(self, looking_for_value: str, raw_value: str):
        super().__init__(f"Unable to parse '{looking_for_value}' from '{raw_value}'")


@dataclass
class Advance:
    """Encodes the advance from one base to another.

    Args:
        from_base: the base the player is coming from
        to_base: the base the player is advancing to
        raw: the raw advance value
    """

    from_base: Base
    to_base: Base
    raw: str

    @classmethod
    def from_event_advance(cls, advance: str) -> "Advance":
        """Load an advance from the advance part of a play's event.

        Args:
            advance: the advance part of a play's event
                Examples include: 'B-1', '2-3'
        """
        bases = advance.split("-")
        return cls(
            from_base=Base(bases[0]),
            to_base=Base(bases[1]),
            raw=advance,
        )


@dataclass
class Out:
    """Encodes a player going out from a play.

    Args:
        from_base: the base the player is coming from
        to_base: the base the player is advancing to
        fielder_position_assists: the fielder positions of players assisting the out
        fielder_position_put_out: the fielder position of the player putting the runner out
        raw: the raw out value
    """

    from_base: Base
    to_base: Base
    fielder_position_assists: list[int]
    fielder_position_put_out: int
    raw: str

    @classmethod
    def from_event_out(cls, out: str) -> "Out":
        """Load an out from the out part of a play's event.

        Args:
            out: the out part of a play's event
                Examples include: '1XH(862)'
        """
        from_base, to_base_raw = out.split("X")
        to_base_match = re.search(r"(.)\(\d+\)", to_base_raw)
        if to_base_match:
            to_base = to_base_match.group(1)
        else:
            raise ParseError("to_base", to_base_raw)

        fielder_positions_match = re.search(r".\((\d+)\)", to_base_raw)
        if fielder_positions_match:
            fielder_positions = fielder_positions_match.group(1)
        else:
            raise ParseError("fielding_positions", to_base_raw)

        return cls(
            from_base=Base(from_base),
            to_base=Base(to_base),
            fielder_position_put_out=int(fielder_positions[-1]),
            fielder_position_assists=[int(p) for p in fielder_positions[:-1]] if len(fielder_positions) > 1 else [],
            raw=out,
        )


@dataclass
class Modifier:
    """Encodes a play modifier.

    Args:
        raw: the raw play modifier
    """

    raw: str

    @classmethod
    def from_event_modifier(cls, modifier: str) -> "Modifier":
        """Load a modifier from the modifier part of a play's event.

        Args:
            modifier: a modifier part of a play's event
                Examples include: @TODO
        """
        return cls(raw=modifier)


@dataclass
class Description:
    """Encodes a basic play description.

    Args:
        raw: the raw play description
    """

    raw: str

    @classmethod
    def from_event_description(cls, description: str) -> "Description":
        """Load a description from the description part of a play's event.

        Args:
            description: the description part of a play's event
                Examples include: @TODO
        """
        return cls(raw=description)


@dataclass
class Event:
    """The event of a play as defined in Retrosheet."""

    description: Description
    modifiers: list[Modifier]
    advances: list[Advance]
    outs: list[Out]
    raw: str

    @classmethod
    def from_play_event(cls, event: str) -> "Event":
        """Load an event from a play line event value.

        Args:
            event: the event description (last part of a play line)
                Examples include: '8/F78', '9/SF.3-H', 'S9/L9S.2-H;1-3'
        """
        # Retrosheet docs indicate these characters at the end of the string can be safely ignored.
        # They indicate sentiment values (uncertainty in a play, hard hit ball, etc.).
        for char in "#!?+-":
            if event.endswith(char):
                event = event[:-1]

        if "." in event:
            description_and_modifiers, advances_and_outs_raw = event.split(".")
            advances_and_outs = advances_and_outs_raw.split(";")
        else:
            description_and_modifiers = event
            advances_and_outs = []

        description, *modifiers = description_and_modifiers.split("/")
        return cls(
            description=Description.from_event_description(description),
            modifiers=[Modifier.from_event_modifier(m) for m in modifiers],
            outs=[Out.from_event_out(o) for o in advances_and_outs if "X" in o],
            advances=[Advance.from_event_advance(a) for a in advances_and_outs if "-" in a],
            raw=event,
        )


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
