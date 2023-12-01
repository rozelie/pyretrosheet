import pytest

from pyretrosheet.models import play


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
