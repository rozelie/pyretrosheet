import pytest

from pyretrosheet.models.base import Base
from pyretrosheet.models.play import advance


@pytest.mark.parametrize(
    ["raw_advance", "expected_from_base", "expected_to_base"],
    [
        ("B-1", Base.BATTER_AT_HOME, Base.FIRST_BASE),
        ("2-H", Base.SECOND_BASE, Base.HOME),
    ],
)
def test__get_bases(raw_advance, expected_from_base, expected_to_base):
    assert advance._get_bases(raw_advance) == (expected_from_base, expected_to_base)


@pytest.mark.parametrize(
    ["raw_advance", "expected_additional_info"],
    [
        ("B-1", []),
        ("2-H(WP)", ["WP"]),
        ("2-H(WP)(TH1)", ["WP", "TH1"]),
    ],
)
def test__get_additional_info(raw_advance, expected_additional_info):
    assert advance._get_additional_info(raw_advance) == expected_additional_info
