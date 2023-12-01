import pytest

from pyretrosheet.models.play import event


@pytest.mark.parametrize(
    "raw_event",
    [
        "PO1(E1/TH).3-H(UR);1-2",
        "99/",
        "15(2)4//BG/GDP.1-2",
        "E2/TH/SH/.1-2",
    ],
)
def test_can_parse_event(raw_event):
    """Various events that were once not parseable - used for regression testing."""
    _ = event.Event.from_play_event(raw_event).modifiers

    # passes if no exception raised
