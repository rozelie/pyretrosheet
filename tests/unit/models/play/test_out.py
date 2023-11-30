import pytest

from pyretrosheet.models.base import Base
from pyretrosheet.models.play import out


@pytest.mark.parametrize(
    ["raw_advance", "expected_from_base", "expected_to_base"],
    [
        ("BX1", Base.BATTER_AT_HOME, Base.FIRST_BASE),
        ("2XH", Base.SECOND_BASE, Base.HOME),
        ("3XH(1E2)", Base.THIRD_BASE, Base.HOME),
    ],
)
def test__get_bases(raw_advance, expected_from_base, expected_to_base):
    assert out._get_bases(raw_advance) == (expected_from_base, expected_to_base)


@pytest.mark.parametrize(
    ["raw_out", "expected_is_actual_out"],
    [
        ("1X2", True),
        ("1X2(1)", True),
        ("BX2(7E4)", False),
    ],
)
def test__is_actual_out(raw_out, expected_is_actual_out):
    assert out._is_actual_out(raw_out) == expected_is_actual_out


@pytest.mark.parametrize(
    ["raw_out", "expected_fielder_assists"],
    [
        # ("1X2", []),
        # ("1X2(1)", []),
        ("BX2(7E4)", [7]),
        ("1X2(13)", [1]),
        ("1X2(123)", [1, 2]),
    ],
)
def test__get_fielder_assists(raw_out, expected_fielder_assists):
    assert out._get_fielder_assists(raw_out) == expected_fielder_assists


@pytest.mark.parametrize(
    ["raw_out", "is_actual_out", "expected_fielder_put_out"],
    [
        ("BX2(7E4)", False, None),
        ("1X2", True, None),
        ("1X2(1)", True, 1),
        ("1X2(13)", True, 3),
        ("1X2(12)", True, 2),
    ],
)
def test__get_fielder_put_out(raw_out, is_actual_out, expected_fielder_put_out):
    assert out._get_fielder_put_out(raw_out, is_actual_out) == expected_fielder_put_out


@pytest.mark.parametrize(
    ["raw_out", "is_actual_out", "expected_fielder_handlers"],
    [
        ("BX2(7E4)", False, [7]),
        ("BX2(27E4)", False, [2, 7]),
        ("BX2(27E45)", False, [2, 7, 5]),
        ("1X2", True, []),
        ("1X2(1)", True, []),
    ],
)
def test__get_fielder_handlers(raw_out, is_actual_out, expected_fielder_handlers):
    assert out._get_fielder_handlers(raw_out, is_actual_out) == expected_fielder_handlers


@pytest.mark.parametrize(
    ["raw_out", "is_actual_out", "expected_fielder_errors"],
    [
        ("BX2(7E4)", False, [4]),
        ("BX2(27E4)", False, [4]),
        ("BX2(27E4E5)", False, [4, 5]),
        ("1X2", True, []),
        ("1X2(1)", True, []),
    ],
)
def test__get_fielder_errors(raw_out, is_actual_out, expected_fielder_errors):
    assert out._get_fielder_errors(raw_out, is_actual_out) == expected_fielder_errors
