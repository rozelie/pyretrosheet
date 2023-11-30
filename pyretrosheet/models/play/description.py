"""Encapsulates Retrosheet play basic description as part of play data."""
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto

from pyretrosheet.models.base import Base


class BatterEvent(Enum):
    """Represents a batter event as part of a play's basic description."""

    UNASSISTED_FIELDED_OUT = auto()
    ASSISTED_FIELDED_OUT = auto()
    GROUNDED_INTO_DOUBLE_PLAY = auto()
    LINED_INTO_DOUBLE_PLAY = auto()
    GROUNDED_INTO_TRIPLE_PLAY = auto()
    LINED_INTO_TRIPLE_PLAY = auto()
    CATCHER_INTERFERENCE = auto()
    SINGLE = auto()
    DOUBLE = auto()
    TRIPLE = auto()
    GROUND_RULE_DOUBLE = auto()
    ERROR = auto()
    FIELDERS_CHOICE = auto()
    ERROR_ON_FOUL_FLY_BALL = auto()
    HOME_RUN_LEAVING_PARK = auto()
    HOME_RUN_INSIDE_PARK = auto()
    HIT_BY_PITCH = auto()
    STRIKEOUT = auto()
    NO_PLAY = auto()
    INTENTIONAL_WALK = auto()
    WALK = auto()


class RunnerEvent(Enum):
    """Represents a runner event as part of a play's basic description."""


@dataclass
class Description:
    """Encodes a basic play description.

    Args:
        batter_event: event performed by the batter, if any
        runner_event: event performed by a runner, if any
        fielder_assists: map of the fielder positions of players to number of assists, if any
        fielder_put_outs: map of the fielder positions of players to number of put outs, if any
        fielder_errors: map of the fielder positions of players to number of errors committed, if any
        fielder_handlers: map of the fielder positions of players to number of times the fielder
            handled the ball for a play that did not result in an out, if any
        put_out_at_base: if a put out is made at a base not normally covered by the fielder,
            the base runner is given explicitly
        raw: the raw play description
    """

    batter_event: BatterEvent | None
    runner_event: RunnerEvent | None
    fielder_assists: dict[int, int]
    fielder_put_outs: dict[int, int]
    fielder_handlers: dict[int, int]
    fielder_errors: dict[int, int]
    put_out_at_base: Base | None
    raw: str

    @classmethod
    def from_event_description(cls, description: str) -> "Description":
        """Load a description from the description part of a play's event.

        Args:
            description: the description part of a play's event
        """
        # @TODO next up is K+event
        batter_event = _get_batter_event(description)
        runner_event = _get_runner_event(description)
        fielding_out_plays = _get_fielding_out_plays(description, batter_event)
        fielding_handler_plays = _get_fielding_handler_plays(description, batter_event)
        return cls(
            batter_event=batter_event,
            runner_event=runner_event,
            fielder_assists=_get_fielder_assists(fielding_out_plays),
            fielder_put_outs=_get_fielder_put_outs(fielding_out_plays),
            fielder_handlers=_get_fielder_handlers(fielding_handler_plays),
            fielder_errors=_get_fielder_errors(description, batter_event),
            put_out_at_base=_get_put_out_at_base(description, batter_event),
            raw=description,
        )


def _get_batter_event(description: str) -> BatterEvent | None:
    """Get the batter event from the description.

    The batter event is encoded at the start of the description, if there is one.

    Args:
        description: the description part of a play's event
    """
    pattern_to_batter_event = {
        r"\d": BatterEvent.UNASSISTED_FIELDED_OUT,
        r"\d{2,}(\(.\))?": BatterEvent.ASSISTED_FIELDED_OUT,
        r"\d+\([123H]\)\d": BatterEvent.GROUNDED_INTO_DOUBLE_PLAY,
        r"\d+\([123H]\)\d\([123H]\)\d": BatterEvent.GROUNDED_INTO_TRIPLE_PLAY,
        r"\d+\(B\)\d+\(.\)": BatterEvent.LINED_INTO_DOUBLE_PLAY,
        r"\d+\(B\)\d+\(.\)\d+\(.\)": BatterEvent.LINED_INTO_TRIPLE_PLAY,
        r"H(R)?": BatterEvent.HOME_RUN_LEAVING_PARK,
        r"H(R)?\d": BatterEvent.HOME_RUN_INSIDE_PARK,
        r"S\d+": BatterEvent.SINGLE,
        r"D\d+": BatterEvent.DOUBLE,
        r"T\d+": BatterEvent.TRIPLE,
        r"E\d": BatterEvent.ERROR,
        r"FLE\d": BatterEvent.ERROR_ON_FOUL_FLY_BALL,
        r"FC\d": BatterEvent.FIELDERS_CHOICE,
        r"C": BatterEvent.CATCHER_INTERFERENCE,
        r"HP": BatterEvent.HIT_BY_PITCH,
        r"DGR": BatterEvent.GROUND_RULE_DOUBLE,
        r"K": BatterEvent.STRIKEOUT,
    }
    for pattern, batter_event in pattern_to_batter_event.items():
        if re.fullmatch(pattern, description):
            return batter_event

    return None


def _get_runner_event(description: str) -> RunnerEvent | None:
    """Get the runner event from the description.

    The runner event is encoded at the start of the description or after a '+' following a
    batter event, if there is one.

    Args:
        description: the description part of a play's event
    """


def _get_fielding_out_plays(description: str, batter_event: BatterEvent | None) -> list[str]:
    """Get the fielding plays resulting in outs.

    Plays in this context is a string that contains the fielding positions of the fielders involved in the out.

    Args:
        description: the description part of a play's event
        batter_event: the batting event, if it exists
    """
    fielding_out_plays: list[str] = []
    match batter_event:
        case BatterEvent.UNASSISTED_FIELDED_OUT:
            fielding_out_plays.append(re.fullmatch(r"(\d)", description).group(1))  # type: ignore

        case BatterEvent.ASSISTED_FIELDED_OUT:
            fielding_out_plays.append(re.fullmatch(r"(\d+).*", description).group(1))  # type: ignore

        case BatterEvent.GROUNDED_INTO_DOUBLE_PLAY:
            match = re.fullmatch(r"(\d+)\(.\)(\d+)", description)
            fielding_out_plays.extend(match.group(g) for g in [1, 2])  # type: ignore

        case BatterEvent.GROUNDED_INTO_TRIPLE_PLAY:
            match = re.fullmatch(r"(\d+)\(.\)(\d+)\(.\)(\d+)", description)
            fielding_out_plays.extend(match.group(g) for g in [1, 2, 3])  # type: ignore

        case BatterEvent.LINED_INTO_DOUBLE_PLAY:
            match = re.fullmatch(r"(\d+)\(.\)(\d+)\(.\)", description)
            fielding_out_plays.extend(match.group(g) for g in [1, 2])  # type: ignore

        case BatterEvent.LINED_INTO_TRIPLE_PLAY:
            match = re.fullmatch(r"(\d+)\(.\)(\d+)\(.\)(\d+)\(.\)", description)
            fielding_out_plays.extend(match.group(g) for g in [1, 2, 3])  # type: ignore

    # @TODO match runner_event
    return fielding_out_plays


def _get_fielding_handler_plays(description: str, batter_event: BatterEvent | None) -> list[str]:
    """Get fielding handler plays (plays that did not result in error or outs).

    Plays in this context is a string that contains the fielding positions of the fielders involved in the handling
    of the play.

    Args:
        description: the description part of a play's event
        batter_event: the batting event, if it exists
    """
    fielding_handler_plays: list[str] = []
    match batter_event:
        case BatterEvent.SINGLE | BatterEvent.DOUBLE | BatterEvent.TRIPLE | BatterEvent.FIELDERS_CHOICE | BatterEvent.HOME_RUN_INSIDE_PARK:
            match = re.fullmatch(r"(S|D|T|FC|H|HR)(\d+)", description)
            fielding_handler_plays.append(match.group(2))  # type: ignore

    # @TODO match runner_event
    return fielding_handler_plays


def _get_fielder_assists(fielding_out_plays: list[str]) -> dict[int, int]:
    """Get a map of fielder positions and the number of assists they made on the play.

    Args:
        fielding_out_plays: plays where fielding outs occurred
    """
    fielder_assists: defaultdict[int, int] = defaultdict(int)
    for play in fielding_out_plays:
        if len(play) == 0:
            continue

        for fielder_position in play[:-1]:
            fielder_assists[int(fielder_position)] += 1

    return dict(fielder_assists)


def _get_fielder_put_outs(fielding_out_plays: list[str]) -> dict[int, int]:
    """Get a map of fielder positions and the number of put outs they made on the play.

    Args:
        fielding_out_plays: plays where fielding outs occurred
    """
    fielder_put_outs: defaultdict[int, int] = defaultdict(int)
    for play in fielding_out_plays:
        put_out_position = int(play[-1])
        fielder_put_outs[put_out_position] += 1

    return dict(fielder_put_outs)


def _get_fielder_handlers(fielding_handler_plays: list[str]) -> dict[int, int]:
    """Get a map of fielder positions and the number of handling actions they made on the play.

    Args:
        fielding_handler_plays: plays where fielding handling occurred
    """
    fielder_handlers: defaultdict[int, int] = defaultdict(int)
    for play in fielding_handler_plays:
        for fielder_position in play:
            fielder_handlers[int(fielder_position)] += 1

    return dict(fielder_handlers)


def _get_fielder_errors(description: str, batter_event: BatterEvent | None) -> dict[int, int]:
    """Get a map of fielder positions and the number of errors they made on the play.

    Args:
        description: the description part of a play's event
        batter_event: the batting event, if it exists
    """
    fielder_errors: defaultdict[int, int] = defaultdict(int)
    match batter_event:
        case BatterEvent.ERROR:
            match = re.fullmatch(r"E(\d+)", description)
            for fielder_position in match.group(1):  # type: ignore
                fielder_errors[int(fielder_position)] += 1

        case BatterEvent.ERROR_ON_FOUL_FLY_BALL:
            match = re.fullmatch(r"FLE(\d+)", description)
            for fielder_position in match.group(1):  # type: ignore
                fielder_errors[int(fielder_position)] += 1

    return dict(fielder_errors)


def _get_put_out_at_base(description: str, batter_event: BatterEvent | None) -> Base | None:
    """Get the base of a put out if it's a non-conventional base put out at.

    Args:
        description: the description part of a play's event
        batter_event: the batting event, if it exists
    """
    if batter_event == BatterEvent.ASSISTED_FIELDED_OUT:
        match = re.fullmatch(r"\d+\((.)\)", description)
        if match:
            return Base(match.group(1))

    return None
