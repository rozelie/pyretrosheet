"""Encapsulates Retrosheet event as part of play data."""
import re
from dataclasses import dataclass

from pyretrosheet.models.exceptions import ParseError
from pyretrosheet.models.play.advance import Advance
from pyretrosheet.models.play.description import Description
from pyretrosheet.models.play.modifier import Modifier


@dataclass
class Event:
    """The event of a play as defined in Retrosheet."""

    description: Description
    modifiers: list[Modifier]
    advances: list[Advance]
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
        for char in "#!?+-/":
            if event.endswith(char):
                event = event[:-1]

        # need to handle this case specifically as to not make the rest of the logic more complex
        # this is the only known case of multiple '.' in a play - likely an encoding error
        if event == "FC3/DP/G3S.3XH(32);1X2(8).B-1":
            description_and_modifiers = "FC3/DP/G3S"
            advances = ["3XH(32)", "1X2(8)", "B-1"]
        elif "." in event:
            description_and_modifiers, advances_raw = event.split(".")
            advances = advances_raw.split(";")
        else:
            description_and_modifiers = event
            advances = []

        # there are cases of double slashes which I do not believe adds any extra info - remove them
        description_and_modifiers = description_and_modifiers.replace("//", "/")

        # remove trailing slashes - does not encode anything
        if description_and_modifiers.endswith("/"):
            description_and_modifiers = description_and_modifiers[:-1]

        # I shamelessly used ChatGPT for this pattern since it's difficult to separate the description and modifiers
        # consistently.
        # Examples (description and modifiers split out):
        # A => 'A', []
        # A/B/C => 'A', ['B', 'C']
        # A(1/2) => 'A(1/2)', []
        # A(1/2)/B => 'A(1/2)', ['B']
        pattern = re.compile(r"^([^/]+(?:/[^/(]+(?:\([^)]*\))?[^/]*)*)$")
        match = pattern.match(description_and_modifiers)
        try:
            description = match.group(1)  # type: ignore
            modifiers = [group for group in match.groups()[1:] if group is not None]  # type: ignore
        except AttributeError as e:
            raise ParseError("description_and_modifiers", event) from e

        return cls(
            description=Description.from_event_description(description),
            modifiers=[Modifier.from_event_modifier(m) for m in modifiers],
            advances=[Advance.from_event_advance(a) for a in advances],
            raw=event,
        )
