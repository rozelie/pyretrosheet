"""Encapsulates Retrosheet advances as part of play data."""
import re
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum

from pyretrosheet.models.base import Base
from pyretrosheet.models.exceptions import ParseError


class RunAccreditation(Enum):
    """Accreditations for a run."""

    UNEARNED_RUN = "UR"
    RBI_CREDITED = "RBI"
    RBI_NOT_CREDITED = "NORBI"
    RBI_NOT_CREDITED_2 = "NR"
    TEAM_UNEARNED_RUN = "TUR"


@dataclass
class Advance:
    """Encodes the advance from one base to another.

    Note this also includes outs.

    Args:
        from_base: the base the player is coming from
        to_base: the base the player is advancing to
        additional_info: some advances encode additional info
        fielder_assists: map of the fielder positions of players to number of assists, if any
        fielder_put_out: the fielder position of the player putting the runner out, if any player does a put out
        fielder_errors: map of the fielder positions of players to number of errors committed, if any
        fielder_handlers: map of the fielder positions of players to number of times the fielder
            handled the ball for a play that did not result in a real out, if any
        is_out: the advance results in the runner being out
        is_unearned_run_explicit: if a run is explicitly unearned
        is_rbi_credited_explicit: if a run has an explicit rbi credited
        is_rbi_not_credited_explicit: if a run has an explicit rbi not credited
        is_team_unearned_run_explicit: if a run is explicitly a team unearned run
        raw: the raw advance value
    """

    from_base: Base
    to_base: Base
    additional_info: list[str]
    fielder_assists: list[int]
    fielder_put_out: int | None
    fielder_handlers: list[int]
    fielder_errors: list[int]
    is_out: bool
    is_unearned_run_explicit: bool
    is_rbi_credited_explicit: bool
    is_rbi_not_credited_explicit: bool
    is_team_unearned_run_explicit: bool
    raw: str

    @classmethod
    def from_event_advance(cls, advance: str) -> "Advance":
        """Load an advance from the advance part of a play's event.

        Args:
            advance: the advance part of a play's event
                Examples include: 'B-1', '2-3', '1-2(WP)', '2-H(TUR)', '2-H(E4/TH)(UR)(NR)', '1X2', '1XH(862)'
        """
        from_base, to_base = _get_bases(advance)
        additional_info = _get_additional_info(advance)
        is_out = _is_out(advance)
        return cls(
            from_base=from_base,
            to_base=to_base,
            additional_info=_get_additional_info(advance),
            fielder_assists=_get_fielder_assists(additional_info),
            fielder_put_out=_get_fielder_put_out(additional_info, is_out),
            fielder_handlers=_get_fielder_handlers(additional_info, is_out),
            fielder_errors=_get_fielder_errors(additional_info, is_out),
            is_out=is_out,
            is_unearned_run_explicit=RunAccreditation.UNEARNED_RUN.value in additional_info,
            is_rbi_credited_explicit=RunAccreditation.RBI_CREDITED.value in additional_info,
            is_rbi_not_credited_explicit=(
                RunAccreditation.RBI_NOT_CREDITED.value in additional_info
                or RunAccreditation.RBI_NOT_CREDITED_2.value in additional_info
            ),
            is_team_unearned_run_explicit=RunAccreditation.TEAM_UNEARNED_RUN.value in additional_info,
            raw=advance,
        )


def _get_bases(advance: str) -> tuple[Base, Base]:
    """Get from and to bases from the advance.

    Args:
        advance: the advance description
    """
    match = re.fullmatch(r"([B123H])[-X]([B123H]).*", advance)
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


def _is_out(advance: str) -> bool:
    """Determine if the runner is out as a result of the advance.

    If there is an error within an out, the out does not occur.

    Retrosheet Spec:
        The error indicator negates the out.

    Args:
        advance: the advance description
    """
    is_out_encoded = bool(re.fullmatch(r"([B123H])X([B123H]).*", advance))
    has_error = bool(re.search(r"\(.*E.*\)", advance))
    return is_out_encoded and not has_error


def _get_fielder_assists(additional_info: list[str]) -> list[int]:
    """Get fielder position numbers of fielders with an assist.

    Note that fielders are still given an assist even if an error follows them and an actual out does not occur,

    Args:
        additional_info: advance additional info
    """
    fielder_assists = []
    for info in _iter_fielding_additional_info(additional_info):
        for i, fielder_position in enumerate(info):
            if fielder_position == "E" or info[i - 1] == "E" or i == len(info) - 1:
                continue

            fielder_assists.append(int(fielder_position))

    return fielder_assists


def _get_fielder_put_out(additional_info: list[str], is_out: bool) -> int | None:
    """Get the fielder position putting the runner out, if they exist.

    Args:
        additional_info: advance additional info
        is_out: if an out occurs
    """
    if not is_out:
        return None

    for info in _iter_fielding_additional_info(additional_info):
        return int(info[-1])

    return None


def _get_fielder_handlers(additional_info: list[str], is_out: bool) -> list[int]:
    """Get fielder position numbers of fielders handling the ball in the case of not an actual out occurring.

    Args:
        additional_info: advance additional info
        is_out: if an out occurs
    """
    if is_out:
        return []

    fielder_handlers = []
    for info in _iter_fielding_additional_info(additional_info):
        for i, fielder_position in enumerate(info):
            if fielder_position == "E" or info[i - 1] == "E":
                continue

            fielder_handlers.append(int(fielder_position))

    return fielder_handlers


def _get_fielder_errors(additional_info: list[str], is_out: bool) -> list[int]:
    """Get fielder position numbers of fielders committing an error on the out.

    Args:
        additional_info: advance additional info
        is_out: if an out occurs
    """
    if is_out:
        return []

    fielder_errors = []
    for info in _iter_fielding_additional_info(additional_info):
        for i, fielder_position in enumerate(info):
            if fielder_position == "E":
                fielder_errors.append(int(info[i + 1]))

    return fielder_errors


def _iter_fielding_additional_info(additional_info: list[str]) -> Iterator[str]:
    """Iterate additional info and any sub-parts (delimited by '/').

    Args:
        additional_info: advance additional info
    """
    # ignore parts that are not useful in fielding calculations
    ignore_parts_re = r"(WP|TH(\d)?|PB|THH|BR|OBS|(B|R)INT|INT|AP)"
    for info in additional_info:
        for part in info.split("/"):
            corrected_part = part
            # ! encodes an exceptional part of a play, of which we can ignore here
            if "!" in part:
                corrected_part = part.replace("!", "")

            if re.fullmatch(ignore_parts_re, corrected_part):
                continue

            # it is unclear what info like `8-2` represents
            if re.fullmatch(r"\d-\d", corrected_part):
                continue

            # it is unclear what info like `5X` represents
            if re.fullmatch(r"\dX", corrected_part):
                continue

            # it is unclear what info like `74H` represents
            if re.fullmatch(r"\d+H", corrected_part):
                continue

            # run accreditations do not encode any fielding info
            try:
                RunAccreditation(corrected_part)
                continue
            except ValueError:
                pass

            yield corrected_part
