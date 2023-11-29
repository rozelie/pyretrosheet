"""Encapsulates Retrosheet advances as part of play data."""
from dataclasses import dataclass

from pyretrosheet.models.base import Base


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
