from pyretrosheet.models import game
from tests import testing_data

MODULE_PATH = "pyretrosheet.models.game"


class TestGame:
    def test_from_game_lines(self):
        game_lines = testing_data.WAS_2022_SINGLE_GAME_EXAMPLE.read_text().splitlines()

        game_ = game.Game.from_game_lines(game_lines)

        assert game_.game_id.raw == "id,WAS202204070"
        assert game_.home_team_id == "WAS"
        assert game_.visiting_team_id == "NYN"
        assert len(game_.chronological_events) == 129
        assert game_.earned_runs == {
            "aranv001": 0,
            "corbp001": 2,
            "diaze006": 0,
            "lugos001": 0,
            "macha003": 1,
            "may-t001": 1,
            "megit002": 0,
            "murpp001": 0,
            "ottaa001": 0,
            "thomm005": 0,
            "votha001": 2,
        }
