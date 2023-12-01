from pyretrosheet import load
from tests import testing_data

MODULE_PATH = "pyretrosheet.load"


def test_load_games(mocker):
    year = 2022

    games_in_year = list(
        load.load_games(
            data_dir=testing_data.TEST_DATA_DIR,
            year=year,
        )
    )

    # the amount of games encoded in data files in the tests.data dir
    # when this test breaks because more data was added, I'm sorry :(
    assert len(games_in_year) == 3


def test__iter_games_from_play_by_play_file():
    play_by_play_file = testing_data.WAS_2022_TWO_GAME_EXAMPLE

    games = list(load._iter_games_from_play_by_play_file(play_by_play_file))

    game_one, game_two = games
    assert game_one.game_id.raw == "id,WAS202204070"
    assert game_two.game_id.raw == "id,WAS202204080"
