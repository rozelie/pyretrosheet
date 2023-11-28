import pytest

from pyretrosheet import load
from tests import testing_data

MODULE_PATH = "pyretrosheet.load"


@pytest.mark.skip(reason="Game loading not yet implemented")
def test_yield_games_in_year(mocker):
    retrosheet_client = mocker.Mock()
    year = 2022

    games_in_year = list(
        load.yield_games_in_year(
            retrosheet_client=retrosheet_client,
            data_dir=testing_data.TEST_DATA_DIR,
            year=year,
        )
    )


def test__yield_game_lines():
    game_lines_data = testing_data.WAS_2022_TWO_GAME_EXAMPLE.read_text().splitlines()

    game_lines = list(load._yield_game_lines(game_lines_data))

    first_game_lines, second_game_lines = game_lines
    assert len(game_lines) == 2
    assert first_game_lines[0] == "id,WAS202204070"
    assert first_game_lines[-1] == "data,er,murpp001,0"
    assert second_game_lines[0] == "id,WAS202204080"
    assert second_game_lines[-1] == "data,er,murpp001,0"
