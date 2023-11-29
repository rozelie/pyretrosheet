"""Encapsulates Retrosheet play basic description as part of play data."""

from dataclasses import dataclass


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
