import datetime as dt

from pyretrosheet.models import game_id

MODULE_PATH = "pyretrosheet.models.game"


class TestGameId:
    def test_from_retrosheet_id_line(self):
        id_line = "id,ATL198304080"

        game_id_ = game_id.GameID.from_retrosheet_id_line(id_line)

        assert game_id_.home_team_id == "ATL"
        assert game_id_.date == dt.date(year=1983, month=4, day=8)
        assert game_id_.game_number == 0
        assert game_id_.raw == id_line
