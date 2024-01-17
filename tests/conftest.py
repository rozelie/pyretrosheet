from copy import deepcopy

import pytest

from pyretrosheet.models import game
from pyretrosheet.models.play import Play
from pyretrosheet.models.player import Player
from pyretrosheet.models.team import TeamLocation
from tests import testing_data


@pytest.fixture
def player_1():
    return Player(
        id="player001",
        name="Player One",
        team_location=TeamLocation.HOME,
        batting_order_position=0,
        fielding_position=0,
        is_sub=False,
        raw="",
    )


@pytest.fixture
def player_2(player_1):
    player_2 = deepcopy(player_1)
    player_2.id = "player001"
    player_2.name = "Player Two"
    return player_2


@pytest.fixture
def play_single(player_1):
    return Play.from_play_line(play_line=f"play,1,0,{player_1.id},??,X,S", comment_lines=[])


@pytest.fixture
def real_game():
    game_lines = testing_data.WAS_2022_SINGLE_GAME_EXAMPLE.read_text().splitlines()
    return game.Game.from_game_lines(game_lines)
