"""Encapsulates Retrosheet modifiers as part of play data."""

import re
from dataclasses import dataclass
from enum import Enum, auto

from pyretrosheet.models.base import Base
from pyretrosheet.models.exceptions import ParseError
from pyretrosheet.models.play.ignored import trim_ignored_characters


class ModifierType(Enum):
    """Play modifier type, as defined in the Retrosheet spec.

    Retrosheet Spec:

    Play modifiers and explanations
        Each modifier is preceded by / in a play record.
        As always, % indicates one the four bases and $ indicates a fielder.

        AP    appeal play
        BP    pop up bunt
        BG    ground ball bunt
        BGDP  bunt grounded into double play
        BINT  batter interference
        BL    line drive bunt
        BOOT  batting out of turn
        BP    bunt pop up
        BPDP  bunt popped into double play
        BR    runner hit by batted ball
        C     called third strike
        COUB  courtesy batter
        COUF  courtesy fielder
        COUR  courtesy runner
        DP    unspecified double play
        E$    error on $
        F     fly
        FDP   fly ball double play
        FINT  fan interference
        FL    foul
        FO    force out
        G     ground ball
        GDP   ground ball double play
        GTP   ground ball triple play
        IF    infield fly rule
        INT   interference
        IPHR  inside the park home run
        L     line drive
        LDP   lined into double play
        LTP   lined into triple play
        MREV  manager challenge of call on the field
        NDP   no double play credited for this play
        OBS   obstruction (fielder obstructing a runner)
        P     pop fly
        PASS  a runner passed another runner and was called out
        R$    relay throw from the initial fielder to $ with no out made
        RINT  runner interference
        SF    sacrifice fly
        SH    sacrifice hit (bunt)
        TH    throw
        TH%   throw to base %
        TP    unspecified triple play
        UINT  umpire interference
        UREV  umpire review of call on the field
    """

    APPEAL_PLAY = auto()
    POP_UP_BUNT = auto()
    GROUND_BALL_BUNT = auto()
    BUNT_GROUNDED_INTO_DOUBLE_PLAY = auto()
    BATTER_INTERFERENCE = auto()
    LINE_DRIVE_BUNT = auto()
    BATTING_OUT_OF_TURN = auto()
    BUNT_POP_UP = auto()
    BUNT_POPPED_INTO_DOUBLE_PLAY = auto()
    RUNNER_HIT_BY_BATTED_BALL = auto()
    CALLED_THIRD_STRIKE = auto()
    COURTESY_BATTER = auto()
    COURTESY_FIELDER = auto()
    COURTESY_RUNNER = auto()
    UNSPECIFIED_DOUBLE_PLAY = auto()
    ERROR = auto()
    FLY = auto()
    FLY_BALL_DOUBLE_PLAY = auto()
    FAN_INTERFERENCE = auto()
    FOUL = auto()
    FORCE_OUT = auto()
    GROUND_BALL = auto()
    GROUND_BALL_DOUBLE_PLAY = auto()
    GROUND_BALL_TRIPLE_PLAY = auto()
    INFIELD_FLY_RULE = auto()
    INTERFERENCE = auto()
    INSIDE_THE_PARK_HOME_RUN = auto()
    LINE_DRIVE = auto()
    LINED_INTO_DOUBLE_PLAY = auto()
    LINED_INTO_TRIPLE_PLAY = auto()
    MANAGER_CHALLENGE_OF_CALL_ON_THE_FIELD = auto()
    NO_DOUBLE_PLAY_CREDITED_FOR_THIS_PLAY = auto()
    OBSTRUCTION = auto()
    POP_FLY = auto()
    RUNNER_PASSED = auto()
    RELAY_THROW = auto()
    RUNNER_INTERFERENCE = auto()
    SACRIFICE_FLY = auto()
    SACRIFICE_HIT_BUNT = auto()
    THROW = auto()
    UNSPECIFIED_TRIPLE_PLAY = auto()
    UMPIRE_INTERFERENCE = auto()
    UMPIRE_REVIEW_OF_CALL_ON_THE_FIELD = auto()
    HIT_LOCATION = auto()
    # Unsure what these modifiers encode, but they appear frequently enough to define
    B = auto()
    BF = auto()
    BFDP = auto()
    U = auto()
    S = auto()
    RR = auto()
    # These may be typos and the intention was to encode these as their capital letter
    p = auto()
    l = auto()


@dataclass
class Modifier:
    """Encodes a play modifier.

    Args:
        type: the type of modifier, as defined in Retrosheet spec
        hit_location: a hit location, if it exists
        fielder_positions: fielder positions relevant to the modifier, if they exist
        base: a base relevant to the modifier, if it exists
        raw: the raw play modifier
    """

    type: ModifierType
    hit_location: str | None
    fielder_positions: list[int]
    base: Base | None
    raw: str

    @classmethod
    def from_event_modifier(cls, modifier: str) -> "Modifier":
        """Load a modifier from the modifier part of a play's event.

        Args:
            modifier: a modifier part of a play's event
        """
        trimmed_modifier = trim_ignored_characters(modifier)
        modifier_type = _get_modifier_type(trimmed_modifier)
        return cls(
            type=modifier_type,
            hit_location=_get_hit_location(trimmed_modifier, modifier_type),
            fielder_positions=_get_fielder_positions(trimmed_modifier, modifier_type),
            base=_get_base(trimmed_modifier, modifier_type),
            raw=modifier,
        )


def _get_modifier_type(modifier: str) -> ModifierType:
    """Get the modifier type via the raw the modifier.

    Args:
        modifier: a modifier part of a play's event
    """
    # Handle odd case from play in 2004CHA.EVA: 'play,8,0,blakc001,20,BBX,8/!F'
    if modifier == "!F":
        return ModifierType.FLY

    # Handle odd case from play in 2011TEX.EVA: 'play,8,0,swisn001,12,BFCX,5/P!5F'
    if modifier == "P!5F":
        return ModifierType.POP_FLY

    # (\d+.*)? matches hit location which is an optional amount of digits followed by an optional amount
    # of alphabetic characters
    # @TODO: move these to the enum - a tuple of regecies?
    pattern_to_modifier_type = {
        r"AP(\d+.*)?": ModifierType.APPEAL_PLAY,
        r"BP(\d+.*)?": ModifierType.POP_UP_BUNT,
        r"BG(\d+.*)?": ModifierType.GROUND_BALL_BUNT,
        r"BGDP(\d+.*)?": ModifierType.BUNT_GROUNDED_INTO_DOUBLE_PLAY,
        r"BINT(\d+.*)?": ModifierType.BATTER_INTERFERENCE,
        r"BL(\d+.*)?": ModifierType.LINE_DRIVE_BUNT,
        r"BOOT(\d+.*)?": ModifierType.BATTING_OUT_OF_TURN,
        r"BPDP(\d+.*)?": ModifierType.BUNT_POPPED_INTO_DOUBLE_PLAY,
        r"BR(\d+.*)?": ModifierType.RUNNER_HIT_BY_BATTED_BALL,
        r"C(\d+.*)?": ModifierType.CALLED_THIRD_STRIKE,
        r"COUB(\d+.*)?": ModifierType.COURTESY_BATTER,
        r"COUF(\d+.*)?": ModifierType.COURTESY_FIELDER,
        r"COUR(\d+.*)?": ModifierType.COURTESY_RUNNER,
        r"DP(\d+.*)?": ModifierType.UNSPECIFIED_DOUBLE_PLAY,
        r"E\d(\d+.*)?": ModifierType.ERROR,
        r"F(\d+.*)?": ModifierType.FLY,
        r"FDP(\d+.*)?": ModifierType.FLY_BALL_DOUBLE_PLAY,
        r"FINT(\d+.*)?": ModifierType.FAN_INTERFERENCE,
        r"FL(\d+.*)?": ModifierType.FOUL,
        r"FO(\d+.*)?": ModifierType.FORCE_OUT,
        r"G(\d+.*)?": ModifierType.GROUND_BALL,
        r"GDP(\d+.*)?": ModifierType.GROUND_BALL_DOUBLE_PLAY,
        r"GTP(\d+.*)?": ModifierType.GROUND_BALL_TRIPLE_PLAY,
        r"IF(\d+.*)?": ModifierType.INFIELD_FLY_RULE,
        r"INT(\d+.*)?": ModifierType.INTERFERENCE,
        r"IPHR(\d+.*)?": ModifierType.INSIDE_THE_PARK_HOME_RUN,
        r"L(\d+.*)?": ModifierType.LINE_DRIVE,
        r"LDP(\d+.*)?": ModifierType.LINED_INTO_DOUBLE_PLAY,
        r"LTP(\d+.*)?": ModifierType.LINED_INTO_TRIPLE_PLAY,
        r"MREV(\d+.*)?": ModifierType.MANAGER_CHALLENGE_OF_CALL_ON_THE_FIELD,
        r"NDP(\d+.*)?": ModifierType.NO_DOUBLE_PLAY_CREDITED_FOR_THIS_PLAY,
        r"OBS(\d+.*)?": ModifierType.OBSTRUCTION,
        r"P(\d+.*)?": ModifierType.POP_FLY,
        r"PASS(\d+.*)?": ModifierType.RUNNER_PASSED,
        r"R\d.*": ModifierType.RELAY_THROW,
        r"R": ModifierType.RELAY_THROW,
        r"RINT(\d+.*)?": ModifierType.RUNNER_INTERFERENCE,
        r"SF(\d+.*)?": ModifierType.SACRIFICE_FLY,
        r"SH(\d+.*)?": ModifierType.SACRIFICE_HIT_BUNT,
        r"TH(\d)?(\d+.*)?(H)?": ModifierType.THROW,
        r"TP(\d+.*)?": ModifierType.UNSPECIFIED_TRIPLE_PLAY,
        r"UINT(\d+.*)?": ModifierType.UMPIRE_INTERFERENCE,
        r"UREV(\d+.*)?": ModifierType.UMPIRE_REVIEW_OF_CALL_ON_THE_FIELD,
        r"\d+.*": ModifierType.HIT_LOCATION,
        # Not defined in Retrosheet, but appears frequently enough to define
        r"B": ModifierType.B,
        r"B\d+.*": ModifierType.B,
        r"BF": ModifierType.BF,
        r"BFDP": ModifierType.BFDP,
        r"U": ModifierType.U,
        r"U\d.*": ModifierType.U,
        r"S": ModifierType.S,
        r"RR.*": ModifierType.RR,
        r"p": ModifierType.p,
        r"l": ModifierType.l,
    }
    for pattern, modifier_type in pattern_to_modifier_type.items():
        if re.fullmatch(pattern, modifier):
            return modifier_type

    raise ParseError("modifer_type", modifier)


def _get_hit_location(modifier: str, modifier_type: ModifierType) -> str | None:
    """Get the hit location from the modifier, if it exists.

    Args:
        modifier: a modifier part of a play's event
        modifier_type: the modifier type
    """
    hit_location_re = r"[A-Z]+(\d+.*)"
    if modifier_type in [ModifierType.ERROR, ModifierType.RELAY_THROW]:
        hit_location_re = r"[ER]\d(\d+)"
    elif modifier_type == ModifierType.THROW:
        hit_location_re = r"TH\d(\d+)"
    elif modifier_type == ModifierType.HIT_LOCATION:
        hit_location_re = r"(.*)"

    if match := re.fullmatch(hit_location_re, modifier):
        return match.group(1)

    return None


def _get_fielder_positions(modifier: str, modifier_type: ModifierType) -> list[int]:
    """Get the fielder positions from the modifier, if they exist.

    Args:
        modifier: a modifier part of a play's event
        modifier_type: the type of modifier
    """
    if modifier_type in [ModifierType.ERROR, ModifierType.RELAY_THROW]:
        # handle rare-case of RELAY_THROW modifier without fielding positions specified
        if modifier == "R":
            return []

        try:
            # From Retrosheet Spec: 'U' appearing in a fielding sequence indicates the fielder handling the ball is unknown'
            # We encode unknown as fielder postiion 0.
            fielder_positions = []
            for position in re.fullmatch(r"[ER](.*)", modifier).group(1):  # type: ignore
                if position == "U":
                    fielder_positions.append(0)
                elif position in ["S", "R", "B", "M", "D", "N"]:
                    # idk what these positions are supposed to be ¯\_(ツ)_/¯
                    # 1997CHN.EVN: 'play,7,0,mondr002,10,BX,S8/G6M/R6S.1-2'
                    # 1996LAN.EVN: 'play,8,0,goodc001,22,.CCBB1X,S6/BG/6MS/R3BU4.1-3(E6/TH);B-2'
                    # 1996COL.EVN: 'play,3,0,burkj001,10,BX,S98/R89M'
                    # 1996SDN.EVN: 'play,11,0,dunss001,10,BX,8/R8RD'
                    # 1996TOR.EVA: 'play,7,1,grees001,00,X,36(1)/FO/G3/R36N'
                    continue
                elif position == "(":
                    # ignore metadata in parenthesis, e.g. 'R3(TH)'
                    break
                else:
                    fielder_positions.append(int(position))
        except (AttributeError, ValueError) as e:
            raise ParseError("fielder_position", raw_value=modifier) from e
        else:
            return fielder_positions

    return []


def _get_base(modifier: str, modifier_type: ModifierType) -> Base | None:
    """Get the base from the modifier, if it exists.

    Args:
        modifier: a modifier part of a play's event
        modifier_type: the type of modifier
    """
    if modifier_type == ModifierType.THROW:  # noqa: SIM102
        if match := re.fullmatch(r"TH(\d|H)", modifier):
            return Base(match.group(1))

    return None
