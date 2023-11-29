"""Encapsulates Retrosheet event as part of play data."""
from dataclasses import dataclass

from pyretrosheet.models.play.advance import Advance
from pyretrosheet.models.play.description import Description
from pyretrosheet.models.play.modifier import Modifier
from pyretrosheet.models.play.out import Out


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
