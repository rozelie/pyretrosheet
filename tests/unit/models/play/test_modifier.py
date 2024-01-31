import pytest

from pyretrosheet.models.base import Base
from pyretrosheet.models.play import modifier
from pyretrosheet.models.play.modifier import ModifierType


@pytest.mark.parametrize(
    ["raw_modifier", "expected_modifier_type"],
    [
        ("AP", ModifierType.APPEAL_PLAY),
        ("BP", ModifierType.POP_UP_BUNT),
        ("BG", ModifierType.GROUND_BALL_BUNT),
        ("BGDP", ModifierType.BUNT_GROUNDED_INTO_DOUBLE_PLAY),
        ("BINT", ModifierType.BATTER_INTERFERENCE),
        ("BL", ModifierType.LINE_DRIVE_BUNT),
        ("BOOT", ModifierType.BATTING_OUT_OF_TURN),
        ("BPDP", ModifierType.BUNT_POPPED_INTO_DOUBLE_PLAY),
        ("BR", ModifierType.RUNNER_HIT_BY_BATTED_BALL),
        ("C", ModifierType.CALLED_THIRD_STRIKE),
        ("COUB", ModifierType.COURTESY_BATTER),
        ("COUF", ModifierType.COURTESY_FIELDER),
        ("COUR", ModifierType.COURTESY_RUNNER),
        ("DP", ModifierType.UNSPECIFIED_DOUBLE_PLAY),
        ("E1", ModifierType.ERROR),
        ("F", ModifierType.FLY),
        ("FDP", ModifierType.FLY_BALL_DOUBLE_PLAY),
        ("FINT", ModifierType.FAN_INTERFERENCE),
        ("FL", ModifierType.FOUL),
        ("FO", ModifierType.FORCE_OUT),
        ("G", ModifierType.GROUND_BALL),
        ("GDP", ModifierType.GROUND_BALL_DOUBLE_PLAY),
        ("GTP", ModifierType.GROUND_BALL_TRIPLE_PLAY),
        ("IF", ModifierType.INFIELD_FLY_RULE),
        ("INT", ModifierType.INTERFERENCE),
        ("IPHR", ModifierType.INSIDE_THE_PARK_HOME_RUN),
        ("L", ModifierType.LINE_DRIVE),
        ("LDP", ModifierType.LINED_INTO_DOUBLE_PLAY),
        ("LTP", ModifierType.LINED_INTO_TRIPLE_PLAY),
        ("MREV", ModifierType.MANAGER_CHALLENGE_OF_CALL_ON_THE_FIELD),
        ("NDP", ModifierType.NO_DOUBLE_PLAY_CREDITED_FOR_THIS_PLAY),
        ("OBS", ModifierType.OBSTRUCTION),
        ("P", ModifierType.POP_FLY),
        ("PASS", ModifierType.RUNNER_PASSED),
        ("R1", ModifierType.RELAY_THROW),
        ("RINT", ModifierType.RUNNER_INTERFERENCE),
        ("SF", ModifierType.SACRIFICE_FLY),
        ("SH", ModifierType.SACRIFICE_HIT_BUNT),
        ("TH", ModifierType.THROW),
        ("TH1", ModifierType.THROW),
        ("TP", ModifierType.UNSPECIFIED_TRIPLE_PLAY),
        ("UINT", ModifierType.UMPIRE_INTERFERENCE),
        ("UREV", ModifierType.UMPIRE_REVIEW_OF_CALL_ON_THE_FIELD),
        ("78", ModifierType.HIT_LOCATION),
        ("B", ModifierType.UNKNOWN),
        ("BF", ModifierType.UNKNOWN),
        ("BFDP", ModifierType.UNKNOWN),
        ("THH", ModifierType.UNKNOWN),
        ("B4S", ModifierType.UNKNOWN),
        ("B34S", ModifierType.UNKNOWN),
        ("B2R", ModifierType.UNKNOWN),
        ("B25", ModifierType.UNKNOWN),
        ("B2L", ModifierType.UNKNOWN),
        ("B23F", ModifierType.UNKNOWN),
        ("B2RF", ModifierType.UNKNOWN),
        ("B6MS", ModifierType.UNKNOWN),
        ("p", ModifierType.UNKNOWN),
        ("U", ModifierType.UNKNOWN),
        ("S", ModifierType.UNKNOWN),
        ("U1", ModifierType.UNKNOWN),
        ("l", ModifierType.UNKNOWN),
        ("U9R4", ModifierType.UNKNOWN),
    ],
)
def test__get_modifier_type(raw_modifier, expected_modifier_type):
    assert modifier._get_modifier_type(raw_modifier) == expected_modifier_type


@pytest.mark.parametrize(
    ["raw_modifier", "modifier_type", "expected_hit_location"],
    [
        ("AP", ModifierType.APPEAL_PLAY, None),
        ("L89S", ModifierType.LINE_DRIVE, "89S"),
        ("E1", ModifierType.ERROR, None),
        ("E12", ModifierType.ERROR, "2"),
        ("R1", ModifierType.RELAY_THROW, None),
        ("R12", ModifierType.RELAY_THROW, "2"),
        ("TH1", ModifierType.THROW, None),
        ("TH12", ModifierType.THROW, "2"),
        ("89", ModifierType.HIT_LOCATION, "89"),
        ("7L", ModifierType.HIT_LOCATION, "7L"),
    ],
)
def test__get_hit_location(raw_modifier, modifier_type, expected_hit_location):
    assert modifier._get_hit_location(raw_modifier, modifier_type) == expected_hit_location


@pytest.mark.parametrize(
    ["raw_modifier", "modifier_type", "expected_fielder_position"],
    [
        ("E1", ModifierType.ERROR, [1]),
        ("R1", ModifierType.RELAY_THROW, [1]),
        ("R25", ModifierType.RELAY_THROW, [2, 5]),
    ],
)
def test__get_fielder_positions(raw_modifier, modifier_type, expected_fielder_position):
    assert modifier._get_fielder_positions(raw_modifier, modifier_type) == expected_fielder_position


@pytest.mark.parametrize(
    ["raw_modifier", "modifier_type", "expected_base"],
    [
        ("TH", ModifierType.THROW, None),
        ("TH1", ModifierType.THROW, Base.FIRST_BASE),
    ],
)
def test__get_base(raw_modifier, modifier_type, expected_base):
    assert modifier._get_base(raw_modifier, modifier_type) == expected_base
