import os

import pytest

import pyretrosheet
from pyretrosheet.models.play.modifier import ModifierType
from pyretrosheet.views import get_plays


@pytest.mark.skipif(not os.getenv("PYRETROSHEET_TEST_ALL_DATA"), reason="I/O intensive and should only be run locally")
def test_all_data_loading(tmp_path):
    """Loads all Retrosheet data and confirms that all data is at the very least loadable.

    Also asserts the total number of UNKNOWN modifiers to ensure they are being loaded (at least mostly) properly
    and that only a few exceptions are present per year.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    start_year = 1919
    end_year = 2022
    unknown_modifiers_per_year_threshold = 100

    print(f"\nTesting all data from {start_year=} to {end_year=}")
    for year in range(start_year, end_year + 1):
        print(f"Testing {year=}...")
        games = list(pyretrosheet.load_games(year, data_dir))
        unknown_modifiers = _get_unknown_modifiers(games)
        print(f"- Found {len(unknown_modifiers)} unknown modifiers")
        if len(unknown_modifiers) > unknown_modifiers_per_year_threshold:
            for unknown_modifier in unknown_modifiers:
                print(f"  - {unknown_modifier}")

        assert len(unknown_modifiers) < unknown_modifiers_per_year_threshold


def _get_unknown_modifiers(games):
    unknown_modifiers = []
    for game in games:
        for play in get_plays(game):
            for modifier in play.event.modifiers:
                if modifier.type == ModifierType.UNKNOWN:
                    unknown_modifiers.append(f"{modifier.raw=} | {play.raw=}")

    return unknown_modifiers
