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
        fielder_assists: map of the fielder positions of players to number of assists, if any
        fielder_put_out: the fielder position of the player putting the runner out, if any player does a put out
        fielder_errors: map of the fielder positions of players to number of errors committed, if any
        fielder_handlers: map of the fielder positions of players to number of times the fielder
            handled the ball for a play that did not result in a real out, if any
        is_actual_out: if the out actually puts a player out (e.g. an error in the additional info
            implies no actual out is made)
        raw: the raw out value
    """

    from_base: Base
    to_base: Base
    fielder_assists: list[int]
    fielder_put_out: int | None
    fielder_handlers: list[int]
    fielder_errors: list[int]
    is_actual_out: bool
    raw: str

    @classmethod
    def from_event_out(cls, out: str) -> "Out":
        """Load an out from the out part of a play's event.

        Args:
            out: the out part of a play's event
                Examples include: '1X2', '1XH(862)'
        """
        from_base, to_base = _get_bases(out)
        is_actual_out = _is_actual_out(out)
        return cls(
            from_base=from_base,
            to_base=to_base,
            fielder_assists=_get_fielder_assists(out),
            fielder_put_out=_get_fielder_put_out(out, is_actual_out),
            fielder_handlers=_get_fielder_handlers(out, is_actual_out),
            fielder_errors=_get_fielder_errors(out, is_actual_out),
            is_actual_out=is_actual_out,
            raw=out,
        )


def _get_bases(out: str) -> tuple[Base, Base]:
    """Get from and to bases from the out.

    Args:
        out: the out description
    """
    match = re.fullmatch(r"([B123H])X([B123H]).*", out)
    if not match:
        raise ParseError("bases_from_out", out)

    return Base(match.group(1)), Base(match.group(2))


def _is_actual_out(out: str) -> bool:
    """Determine if the out is an actual out.

    If there is an error within an out, the out does not occur.

    Retrosheet Spec:
        The error indicator negates the out.

    Args:
        out: the out description
    """
    return not bool(re.search(r"\(.*E.*\)", out))


def _get_fielder_assists(out: str) -> list[int]:
    """Get fielder position numbers of fielders with an assist.

    Note that fielders are still given an assist even if an error follows them and an actual out does not occur,

    Args:
        out: the out description
    """
    fielder_assists = []
    if match := re.fullmatch(r".*\((.*)\)", out):
        fielder_positions = match.group(1)
        for i, fielder_position in enumerate(fielder_positions):
            if fielder_position == "E" or fielder_positions[i - 1] == "E" or i == len(fielder_positions) - 1:
                continue

            fielder_assists.append(int(fielder_position))

    return fielder_assists


def _get_fielder_put_out(out: str, is_actual_out: bool) -> int | None:
    """Get the fielder position putting the runner out, if they exist.

    Args:
        out: the out description
        is_actual_out: if the out is an actual out
    """
    if not is_actual_out:
        return None

    if match := re.fullmatch(r".*\((.*)\)", out):
        return int(match.group(1)[-1])

    return None


def _get_fielder_handlers(out: str, is_actual_out: bool) -> list[int]:
    """Get fielder position numbers of fielders handling the ball in the case of not an actual out occurring.

    Args:
        out: the out description
        is_actual_out: if the out is an actual out
    """
    if is_actual_out:
        return []

    fielder_handlers = []
    fielder_positions = re.fullmatch(r".*\((.*)\)", out).group(1)  # type: ignore
    for i, fielder_position in enumerate(fielder_positions):
        if fielder_position == "E" or fielder_positions[i - 1] == "E":
            continue

        fielder_handlers.append(int(fielder_position))

    return fielder_handlers


def _get_fielder_errors(out: str, is_actual_out: bool) -> list[int]:
    """Get fielder position numbers of fielders committing an error on the out.

    Args:
        out: the out description
        is_actual_out: if the out is an actual out
    """
    if is_actual_out:
        return []

    fielder_positions = re.fullmatch(r".*\((.*)\)", out).group(1)  # type: ignore
    return [
        int(fielder_position) for i, fielder_position in enumerate(fielder_positions) if fielder_positions[i - 1] == "E"
    ]
