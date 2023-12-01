import pytest

from pyretrosheet.models import player


@pytest.mark.parametrize(
    "raw_start_or_sub",
    [
        'sub,barfc101,"Clyde,Barfoot",0,9,1',
        'sub,watkg101,"George Watkins,",0,2,7',
        'sub,burgs101,"Burgess,Smoky",0,9,11',
    ],
)
def test_can_parse_start_or_sub_line(raw_start_or_sub):
    """Various start or sub lines that were once not parseable - used for regression testing."""
    _ = player.Player.from_start_or_sub_line(raw_start_or_sub, False)

    # passes if no exception raised
