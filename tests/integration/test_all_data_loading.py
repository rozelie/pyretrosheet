import os

import pytest

import pyretrosheet
from pyretrosheet.models.play.modifier import ModifierType
from pyretrosheet.views import get_plays


@pytest.mark.skipif(not os.getenv("PYRETROSHEET_TEST_ALL_DATA"), reason="I/O intensive and should only be run locally")
def test_all_data_loading(tmp_path):
    """Loads all Retrosheet data and confirms that all data is at the very least loadable."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    start_year = 1919
    end_year = 2022

    print(f"\nTesting all data from {start_year=} to {end_year=}")
    for year in range(start_year, end_year + 1):
        print(f"Testing {year=}...")
        _ = list(pyretrosheet.load_games(year, data_dir))

    # passes if no exception raised
