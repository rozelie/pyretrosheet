"""Encapsulates Retrosheet advances as part of play data."""
import re
from dataclasses import dataclass

from pyretrosheet.models.base import Base
from pyretrosheet.models.exceptions import ParseError


@dataclass
class Advance:
    """Encodes the advance from one base to another.

    Args:
        from_base: the base the player is coming from
        to_base: the base the player is advancing to
        additional_info: some advances encode additional info
        raw: the raw advance value
    """

    from_base: Base
    to_base: Base
    additional_info: list[str]
    raw: str

    @classmethod
    def from_event_advance(cls, advance: str) -> "Advance":
        """Load an advance from the advance part of a play's event.

        Args:
            advance: the advance part of a play's event
                Examples include: 'B-1', '2-3', '1-2(WP)'
        """
        from_base, to_base = _get_bases(advance)
        return cls(
            from_base=from_base,
            to_base=to_base,
            additional_info=_get_additional_info(advance),
            raw=advance,
        )


def _get_bases(advance: str) -> tuple[Base, Base]:
    """Get from and to bases from the advance.

    Args:
        advance: the advance description
    """
    match = re.fullmatch(r"([B123H])-([B123H])", advance)
    if not match:
        raise ParseError("bases_from_advance", advance)

    return Base(match.group(1)), Base(match.group(2))


def _get_additional_info(advance: str) -> list[str]:
    """Get additional info from an advance.

    Retrosheet description:
        Advances may include additional information in the
        form of one or more parameters specified as a parenthesized strings
        of characters. When more than one parameter is given on an advance
        they are individually parenthesized.

    Args:
        advance: the advance description
    """
    return re.findall(r"\(([^)]+)\)", advance)
