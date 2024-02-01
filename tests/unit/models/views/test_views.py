from pyretrosheet import views
from pyretrosheet.models.player import Player

MODULE_PATH = "pyretrosheet.views"


def test_get_plays(real_game):
    plays = views.get_plays(real_game)
    home_plays = views.get_plays(real_game, include_visiting_team=False)
    visiting_plays = views.get_plays(real_game, include_home_team=False)

    assert len(plays) == 94
    assert len(home_plays) == 43
    assert len(visiting_plays) == 51


def test_get_players(real_game):
    players = views.get_players(real_game)
    home_players = views.get_players(real_game, include_visiting_team=False)
    visiting_players = views.get_players(real_game, include_home_team=False)

    assert len(players) == 35
    assert len(home_players) == 15
    assert len(visiting_players) == 20


def test_get_batter_plays(real_game):
    batter_plays = views.get_batter_plays(real_game)
    home_batter_plays = views.get_batter_plays(real_game, include_visiting_team=False)
    visiting_batter_plays = views.get_batter_plays(real_game, include_home_team=False)

    assert len(batter_plays) == 19
    assert len(home_batter_plays) == 9
    assert len(visiting_batter_plays) == 10


def test_get_inning_plays(real_game):
    inning_plays = views.get_inning_plays(real_game)
    home_inning_plays = views.get_inning_plays(real_game, include_visiting_team=False)
    visiting_inning_plays = views.get_inning_plays(real_game, include_home_team=False)

    assert len(inning_plays) == 9
    assert len(inning_plays[1]) == 8
    assert len(home_inning_plays) == 9
    assert len(home_inning_plays[1]) == 3
    assert len(visiting_inning_plays) == 9
    assert len(visiting_inning_plays[1]) == 5


def test_team_players(real_game):
    games = [real_game]
    team_id = "WAS"

    team_players = views.get_team_players(games, team_id)

    assert len(team_players) == 15
    for player in team_players:
        assert isinstance(player, Player)
