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
        ("!F", ModifierType.FLY),
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
        ("P!5F", ModifierType.POP_FLY),
        ("PASS", ModifierType.RUNNER_PASSED),
        ("R1", ModifierType.RELAY_THROW),
        ("R", ModifierType.RELAY_THROW),
        ("R4U8R5", ModifierType.RELAY_THROW),
        ("R3BU4", ModifierType.RELAY_THROW),
        ("RINT", ModifierType.RUNNER_INTERFERENCE),
        ("SF", ModifierType.SACRIFICE_FLY),
        ("SH", ModifierType.SACRIFICE_HIT_BUNT),
        ("TH", ModifierType.THROW),
        ("TH1", ModifierType.THROW),
        ("THH", ModifierType.THROW),
        ("TP", ModifierType.UNSPECIFIED_TRIPLE_PLAY),
        ("UINT", ModifierType.UMPIRE_INTERFERENCE),
        ("UREV", ModifierType.UMPIRE_REVIEW_OF_CALL_ON_THE_FIELD),
        ("78", ModifierType.HIT_LOCATION),
        ("BF", ModifierType.BF),
        ("B", ModifierType.B),
        ("BFDP", ModifierType.BFDP),
        ("B4S", ModifierType.B),
        ("B34S", ModifierType.B),
        ("B2R", ModifierType.B),
        ("B25", ModifierType.B),
        ("B2L", ModifierType.B),
        ("B23F", ModifierType.B),
        ("B2RF", ModifierType.B),
        ("B6MS", ModifierType.B),
        ("p", ModifierType.p),
        ("U", ModifierType.U),
        ("U1", ModifierType.U),
        ("l", ModifierType.l),
        ("U9R4", ModifierType.U),
        ("U4R6", ModifierType.U),
        ("U4R6", ModifierType.U),
        ("U7R64", ModifierType.U),
        ("U6R5U1", ModifierType.U),
        ("RR6", ModifierType.RR),
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
