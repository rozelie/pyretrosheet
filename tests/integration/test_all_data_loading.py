import os

import pytest

import pyretrosheet


@pytest.mark.skipif(not os.getenv("PYRETROSHEET_TEST_ALL_DATA"), reason="I/O intensive and should only be run locally")
def test_all_data_loading(tmp_path):
    """Loads all Retrosheet data and confirms that all data is at the very least loadable."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    for year in range(1919, 2023):
        print(f"Testing {year=}...")
        list(pyretrosheet.load_games(year, data_dir))

    # passes if no exception raised
