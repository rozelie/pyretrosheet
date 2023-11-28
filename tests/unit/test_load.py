from pyretrosheet import load
from tests import testing_data

MODULE_PATH = "pyretrosheet.load"


def test__yield_game_lines():
    game_lines_data = testing_data.get_game_lines().splitlines()

    game_lines = list(load._yield_game_lines(game_lines_data))

    first_game_lines, second_game_lines = game_lines
    assert len(game_lines) == 2
    assert first_game_lines[0] == "id,WAS202204070"
    assert first_game_lines[-1] == "data,er,murpp001,0"
    assert second_game_lines[0] == "id,WAS202204080"
    assert second_game_lines[-1] == "data,er,murpp001,0"
