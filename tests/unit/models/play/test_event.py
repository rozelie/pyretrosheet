import pytest

from pyretrosheet.models.play import event

@pytest.mark.parametrize(
    ["raw_event", "expected_modifiers"],
    [
        ("PO1(E1/TH).3-H(UR);1-2", []),
    ],
)
def test_event_modifiers(raw_event, expected_modifiers):
    assert event.Event.from_play_event(raw_event).modifiers == expected_modifiers