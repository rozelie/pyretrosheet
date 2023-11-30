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


@pytest.mark.parametrize(
    ["raw_advance", "explicit_attr", "is_explicit"],
    [
        ("B-1", "is_unearned_explicit", False),
        ("B-1", "is_rbi_credited_explicit", False),
        ("B-1", "is_rbi_not_credited_explicit", False),
        ("B-1", "is_team_unearned_run_explicit", False),
        ("1-H(UR)", "is_unearned_explicit", True),
        ("1-H(RBI)", "is_rbi_credited_explicit", True),
        ("1-H(NORBI)", "is_rbi_not_credited_explicit", True),
        ("1-H(TUR)", "is_team_unearned_run_explicit", True),
    ],
)
def test_explicit_values(raw_advance, explicit_attr, is_explicit):
    advance_ = advance.Advance.from_event_advance(raw_advance)

    assert getattr(advance_, explicit_attr) == is_explicit
