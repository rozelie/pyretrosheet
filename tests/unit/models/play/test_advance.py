import pytest

from pyretrosheet.models.base import Base
from pyretrosheet.models.play import advance


@pytest.mark.parametrize(
    ["raw_advance", "expected_from_base", "expected_to_base"],
    [
        ("B-1", Base.BATTER_AT_HOME, Base.FIRST_BASE),
        ("2-H", Base.SECOND_BASE, Base.HOME),
        ("BX1", Base.BATTER_AT_HOME, Base.FIRST_BASE),
        ("2XH", Base.SECOND_BASE, Base.HOME),
        ("3XH(1E2)", Base.THIRD_BASE, Base.HOME),
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
    ["raw_advance", "expected_is_out"],
    [
        ("1-2", False),
        ("1-2(E3)", False),
        ("1X2", True),
        ("1X2(1)", True),
        ("BX2(7E4)", False),
    ],
)
def test__is_out(raw_advance, expected_is_out):
    assert advance._is_out(raw_advance) == expected_is_out


@pytest.mark.parametrize(
    ["additional_info", "expected_fielder_assists"],
    [
        ([], []),
        (["1"], []),
        (["7E4"], [7]),
        (["13"], [1]),
        (["123"], [1, 2]),
        (["WP", "NR"], []),
        (["E2"], []),
        (["1E2"], [1]),
    ],
)
def test__get_fielder_assists(additional_info, expected_fielder_assists):
    assert advance._get_fielder_assists(additional_info) == expected_fielder_assists


@pytest.mark.parametrize(
    ["additional_info", "is_out", "expected_fielder_put_out"],
    [
        ([], True, None),
        (["7E4)"], False, None),
        (["1"], True, 1),
        (["13"], True, 3),
    ],
)
def test__get_fielder_put_out(additional_info, is_out, expected_fielder_put_out):
    assert advance._get_fielder_put_out(additional_info, is_out) == expected_fielder_put_out


@pytest.mark.parametrize(
    ["additional_info", "is_out", "expected_fielder_handlers"],
    [
        ([], True, []),
        (["1"], True, []),
        (["7E4"], False, [7]),
        (["27E4"], False, [2, 7]),
        (["27E45"], False, [2, 7, 5]),
        (["1E2/TH"], False, [1]),
    ],
)
def test__get_fielder_handlers(additional_info, is_out, expected_fielder_handlers):
    assert advance._get_fielder_handlers(additional_info, is_out) == expected_fielder_handlers


@pytest.mark.parametrize(
    ["additional_info", "is_out", "expected_fielder_errors"],
    [
        ({"7E4"}, False, [4]),
        ({"27E4"}, False, [4]),
        ({"27E4E5"}, False, [4, 5]),
        ([], True, []),
        ({"1"}, True, []),
    ],
)
def test__get_fielder_errors(additional_info, is_out, expected_fielder_errors):
    assert advance._get_fielder_errors(additional_info, is_out) == expected_fielder_errors


@pytest.mark.parametrize(
    ["raw_advance", "explicit_attr", "is_explicit"],
    [
        ("B-1", "is_unearned_run_explicit", False),
        ("B-1", "is_rbi_credited_explicit", False),
        ("B-1", "is_rbi_not_credited_explicit", False),
        ("B-1", "is_team_unearned_run_explicit", False),
        ("1-H(UR)", "is_unearned_run_explicit", True),
        ("1-H(RBI)", "is_rbi_credited_explicit", True),
        ("1-H(NORBI)", "is_rbi_not_credited_explicit", True),
        ("1-H(TUR)", "is_team_unearned_run_explicit", True),
    ],
)
def test_explicit_values(raw_advance, explicit_attr, is_explicit):
    advance_ = advance.Advance.from_event_advance(raw_advance)

    assert getattr(advance_, explicit_attr) == is_explicit


@pytest.mark.parametrize(
    ["additional_info", "expected_parts"],
    [
        (["WP", "TH", "TH1", "PB", "THH", "BR", "OBS", "8-2", "5X", "BINT", "RINT", "AP", "74H", "INT"], []),
        (["1", "12", "1E1", "8!5", "92!"], ["1", "12", "1E1", "85", "92"]),
    ],
)
def test__iter_fielding_additional_info(additional_info, expected_parts):
    assert list(advance._iter_fielding_additional_info(additional_info)) == expected_parts
