"""Encapsulates Retrosheet modifiers as part of play data."""

from dataclasses import dataclass


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
