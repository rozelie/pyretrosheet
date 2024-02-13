import pytest

from pyretrosheet.models.base import Base
from pyretrosheet.models.play import description
from pyretrosheet.models.play.description import BatterEvent, RunnerEvent


@pytest.mark.parametrize(
    ["raw_description", "expected_batter_event"],
    [
        ("1", BatterEvent.UNASSISTED_FIELDED_OUT),
        ("123", BatterEvent.ASSISTED_FIELDED_OUT),
        ("123(B)", BatterEvent.ASSISTED_FIELDED_OUT),
        ("45(1)3", BatterEvent.GROUNDED_INTO_DOUBLE_PLAY),
        ("45(1)3(2)6", BatterEvent.GROUNDED_INTO_TRIPLE_PLAY),
        ("45(B)3(2)", BatterEvent.LINED_INTO_DOUBLE_PLAY),
        ("45(B)3(2)6(3)", BatterEvent.LINED_INTO_TRIPLE_PLAY),
        ("H", BatterEvent.HOME_RUN_LEAVING_PARK),
        ("HR", BatterEvent.HOME_RUN_LEAVING_PARK),
        ("H1", BatterEvent.HOME_RUN_INSIDE_PARK),
        ("HR1", BatterEvent.HOME_RUN_INSIDE_PARK),
        ("S1", BatterEvent.SINGLE),
        ("S", BatterEvent.SINGLE),
        ("D1", BatterEvent.DOUBLE),
        ("D", BatterEvent.DOUBLE),
        ("T1", BatterEvent.TRIPLE),
        ("T", BatterEvent.TRIPLE),
        ("E1", BatterEvent.ERROR),
        ("1E1", BatterEvent.ERROR),
        ("FC1", BatterEvent.FIELDERS_CHOICE),
        ("FLE1", BatterEvent.ERROR_ON_FOUL_FLY_BALL),
        ("C", BatterEvent.CATCHER_INTERFERENCE),
        ("DGR", BatterEvent.GROUND_RULE_DOUBLE),
        ("HP", BatterEvent.HIT_BY_PITCH),
        ("K", BatterEvent.STRIKEOUT),
        ("W", BatterEvent.WALK),
        ("I", BatterEvent.INTENTIONAL_WALK),
        ("IW", BatterEvent.INTENTIONAL_WALK),
        ("NP", BatterEvent.NO_PLAY),
    ],
)
def test__get_batter_event(raw_description, expected_batter_event):
    assert description._get_batter_event(raw_description) == expected_batter_event


@pytest.mark.parametrize(
    ["raw_description", "expected_runner_event"],
    [
        ("BK", RunnerEvent.BALK),
        ("CS2(12)", RunnerEvent.CAUGHT_STEALING),
        ("DI", RunnerEvent.DEFENSIVE_INDIFFERENCE),
        ("OA", RunnerEvent.OTHER_ADVANCE),
        ("PB", RunnerEvent.PASSED_BALL),
        ("WP", RunnerEvent.WILD_PITCH),
        ("PO1(1)", RunnerEvent.PICKED_OFF),
        ("POCS1(1)", RunnerEvent.PICKED_OFF_CAUGHT_STEALING),
        ("SBH", RunnerEvent.STOLEN_BASE),
    ],
)
def test__get_runner_event(raw_description, expected_runner_event):
    assert description._get_runner_event(raw_description) == expected_runner_event


@pytest.mark.parametrize(
    ["raw_description", "batter_event", "runner_event", "expected_fielding_out_plays"],
    [
        ("1", BatterEvent.UNASSISTED_FIELDED_OUT, None, ["1"]),
        ("123", BatterEvent.ASSISTED_FIELDED_OUT, None, ["123"]),
        ("123(B)", BatterEvent.ASSISTED_FIELDED_OUT, None, ["123"]),
        ("1(1)23", BatterEvent.GROUNDED_INTO_DOUBLE_PLAY, None, ["1", "23"]),
        ("1(1)23(2)4", BatterEvent.GROUNDED_INTO_TRIPLE_PLAY, None, ["1", "23", "4"]),
        ("1(B)23(1)", BatterEvent.LINED_INTO_DOUBLE_PLAY, None, ["1", "23"]),
        ("1(B)23(1)4(2)", BatterEvent.LINED_INTO_TRIPLE_PLAY, None, ["1", "23", "4"]),
        ("CS2(E2)", None, RunnerEvent.CAUGHT_STEALING, []),
        ("CS2(12)", None, RunnerEvent.CAUGHT_STEALING, ["12"]),
        ("CS2(26!)", None, RunnerEvent.CAUGHT_STEALING, ["26"]),
        ("PO(E1)", None, RunnerEvent.PICKED_OFF, []),
        ("PO(1)", None, RunnerEvent.PICKED_OFF, ["1"]),
        ("POCS(E1)", None, RunnerEvent.PICKED_OFF_CAUGHT_STEALING, []),
        ("POCS(1)", None, RunnerEvent.PICKED_OFF_CAUGHT_STEALING, ["1"]),
        ("POCS(1)", None, RunnerEvent.PICKED_OFF_CAUGHT_STEALING, ["1"]),
    ],
)
def test__get_fielding_out_plays(raw_description, batter_event, runner_event, expected_fielding_out_plays):
    assert (
        description._get_fielding_out_plays(raw_description, batter_event, runner_event) == expected_fielding_out_plays
    )


@pytest.mark.parametrize(
    ["raw_description", "batter_event", "runner_event", "expected_fielding_handler_plays"],
    [
        ("S1", BatterEvent.SINGLE, None, ["1"]),
        ("D1", BatterEvent.DOUBLE, None, ["1"]),
        ("T12", BatterEvent.TRIPLE, None, ["12"]),
        ("FC1", BatterEvent.FIELDERS_CHOICE, None, ["1"]),
        ("H1", BatterEvent.HOME_RUN_INSIDE_PARK, None, ["1"]),
        ("HR1", BatterEvent.HOME_RUN_INSIDE_PARK, None, ["1"]),
        ("CS2(E2)", None, RunnerEvent.CAUGHT_STEALING, []),
        ("CS2(1E2)", None, RunnerEvent.CAUGHT_STEALING, ["1"]),
        ("CS2(12)", None, RunnerEvent.CAUGHT_STEALING, []),
        ("PO(E1)", None, RunnerEvent.PICKED_OFF, []),
        ("PO(1)", None, RunnerEvent.PICKED_OFF, []),
        ("PO(E1/TH)", None, RunnerEvent.PICKED_OFF, []),
        ("POCS(E1)", None, RunnerEvent.PICKED_OFF_CAUGHT_STEALING, []),
        ("POCS(1)", None, RunnerEvent.PICKED_OFF_CAUGHT_STEALING, []),
    ],
)
def test__get_fielding_handler_plays(raw_description, batter_event, runner_event, expected_fielding_handler_plays):
    assert (
        description._get_fielding_handler_plays(raw_description, batter_event, runner_event)
        == expected_fielding_handler_plays
    )


def test__get_fielder_assists():
    fielding_out_plays = ["1", "12", "123"]

    fielder_assists = description._get_fielder_assists(fielding_out_plays)

    assert fielder_assists == {1: 2, 2: 1}


def test__get_fielder_put_outs():
    fielding_out_plays = ["1", "21", "12", "123"]

    fielder_assists = description._get_fielder_put_outs(fielding_out_plays)

    assert fielder_assists == {1: 2, 2: 1, 3: 1}


def test__get_fielder_handlers():
    fielding_handler_plays = ["1", "12"]

    fielder_handlers = description._get_fielder_handlers(fielding_handler_plays)

    assert fielder_handlers == {1: 2, 2: 1}


@pytest.mark.parametrize(
    ["raw_description", "batter_event", "runner_event", "expected_fielder_errors"],
    [
        ("E1", BatterEvent.ERROR, None, {1: 1}),
        ("E12", BatterEvent.ERROR, None, {1: 1, 2: 1}),
        ("FLE1", BatterEvent.ERROR_ON_FOUL_FLY_BALL, None, {1: 1}),
        ("CS2(E2)", None, RunnerEvent.CAUGHT_STEALING, {2: 1}),
        ("CS2(1E2)", None, RunnerEvent.CAUGHT_STEALING, {2: 1}),
        ("PO(E1)", None, RunnerEvent.PICKED_OFF, {1: 1}),
        ("POCS(E1)", None, RunnerEvent.PICKED_OFF_CAUGHT_STEALING, {1: 1}),
    ],
)
def test__get_fielder_errors(raw_description, batter_event, runner_event, expected_fielder_errors):
    assert description._get_fielder_errors(raw_description, batter_event, runner_event) == expected_fielder_errors


@pytest.mark.parametrize(
    ["raw_description", "batter_event", "expected_put_out_at_base"],
    [
        ("123", BatterEvent.UNASSISTED_FIELDED_OUT, None),
        ("123(B)", BatterEvent.ASSISTED_FIELDED_OUT, Base.BATTER_AT_HOME),
    ],
)
def test__get_put_out_at_base(raw_description, batter_event, expected_put_out_at_base):
    assert description._get_put_out_at_base(raw_description, batter_event) == expected_put_out_at_base


@pytest.mark.parametrize(
    ["raw_description", "runner_event", "expected_stolen_base"],
    [
        ("K", None, None),
        ("SB2", RunnerEvent.STOLEN_BASE, Base.SECOND_BASE),
        ("K+SB2", RunnerEvent.STOLEN_BASE, Base.SECOND_BASE),
    ],
)
def test__get_stolen_base(raw_description, runner_event, expected_stolen_base):
    assert description._get_stolen_base(raw_description, runner_event) == expected_stolen_base
