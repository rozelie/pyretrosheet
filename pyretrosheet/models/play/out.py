"""Encapsulates Retrosheet outs as part of play data."""
import re
from dataclasses import dataclass

from pyretrosheet.models.base import Base
from pyretrosheet.models.exceptions import ParseError


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
