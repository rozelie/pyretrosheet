import os

import pytest

import pyretrosheet

START_YEAR = 1919
END_YEAR = 2023


@pytest.mark.skipif(not os.getenv("PYRETROSHEET_TEST_ALL_DATA"), reason="I/O intensive and should only be run locally")
@pytest.mark.parametrize(("year"), list(range(START_YEAR, END_YEAR + 1)))
def test_all_data_loading(tmp_path, year):
    """Loads all Retrosheet data and confirms that all data is at the very least loadable."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    _ = list(pyretrosheet.load_games(year, data_dir))

    # passes if no exception raised
