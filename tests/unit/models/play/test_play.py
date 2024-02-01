import pytest

from pyretrosheet.models import play
from pyretrosheet.models.play.description import BatterEvent
from pyretrosheet.models.play.modifier import ModifierType


@pytest.mark.parametrize(
    "raw_play_line",
    [
        "play,3,1,smitj106,??,,43,2-3",
    ],
)
def test_can_parse_play_line(raw_play_line):
    """Various plays that were once not parseable - used for regression testing."""
    _ = play.Play.from_play_line(raw_play_line, [])

    # passes if no exception raised


def test_parses_single():
    raw_play_line = "play,8,0,reyef001,12,CSBX,S8/L89D+"

    play_ = play.Play.from_play_line(raw_play_line, [])

    assert play_.event.description.batter_event == BatterEvent.SINGLE


@pytest.mark.parametrize(
    ["raw_play_line", "modifier_idx", "expected_fielder_positions"],
    [
        ("play,3,1,johnl001,01,CX,T9/L9LD/R35U1", 1, [3, 5, 0, 1]),
        ("play,3,1,brogr001,11,*BSX,S7/L78S/R6U5.1-2", 1, [6, 0, 5]),
        ("play,2,1,alfoe001,21,S111BBC,SB2/R4U8R5.1-3(E2/TH)", 0, [4, 0, 8, 5]),
        ("play,8,1,berrg001,31,*BBBFX,E5/G5L/R3(TH).3-H(NR)(UR)", 1, [3]),
    ],
)
def test_parses_fielder_positions_from_relay_throw(raw_play_line, modifier_idx, expected_fielder_positions):
    play_ = play.Play.from_play_line(raw_play_line, [])
    modifier = play_.event.modifiers[modifier_idx]

    assert modifier.type == ModifierType.RELAY_THROW
    assert modifier.fielder_positions == expected_fielder_positions


def test_is_an_at_bat__true_for_single():
    raw_play_line = "play,1,1,johnl001,01,CX,S"

    play_ = play.Play.from_play_line(raw_play_line, [])

    assert play_.is_an_at_bat() is True
