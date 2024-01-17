"""View model data through various filters."""
from collections import defaultdict

from pyretrosheet.models.game import Game
from pyretrosheet.models.play import Play
from pyretrosheet.models.player import Player
from pyretrosheet.models.team import TeamLocation


def get_plays(game: Game, include_home_team: bool = True, include_visiting_team: bool = True) -> list[Play]:
    """Get plays in a game.

    Args:
        game: the game to get plays for
        include_home_team: include plays for the home team
        include_visiting_team: include plays for the visiting team
    """
    plays = []
    for event in game.chronological_events:
        if isinstance(event, Play):
            play = event
            if play.team_location == TeamLocation.HOME and include_home_team:
                plays.append(play)
            if play.team_location == TeamLocation.VISITING and include_visiting_team:
                plays.append(play)
    return plays


def get_players(game: Game, include_home_team: bool = True, include_visiting_team: bool = True) -> list[Player]:
    """Get players in a game.

    Args:
        game: the game to get players for
        include_home_team: include players from the home team
        include_visiting_team: include players from the visiting team
    """
    players = []
    for event in game.chronological_events:
        if isinstance(event, Player):
            player = event
            if player.team_location == TeamLocation.HOME and include_home_team:
                players.append(player)
            if player.team_location == TeamLocation.VISITING and include_visiting_team:
                players.append(player)
    return players


def get_batter_plays(
    game: Game, include_home_team: bool = True, include_visiting_team: bool = True
) -> dict[str, list[Play]]:
    """Get a map of batter id to their plays in a game.

    Args:
        game: the game to get plays from
        include_home_team: include plays from the home team
        include_visiting_team: include plays from the visiting team
    """
    batter_plays = defaultdict(list)
    for play in get_plays(game, include_home_team=include_home_team, include_visiting_team=include_visiting_team):
        batter_plays[play.batter_id].append(play)
    return dict(batter_plays)


def get_inning_plays(
    game: Game, include_home_team: bool = True, include_visiting_team: bool = True
) -> dict[int, list[Play]]:
    """Get a map of inning number to plays in that inning for a game.

    Args:
        game: the game to get plays per inning from
        include_home_team: include plays per inning from the home team
        include_visiting_team: include plays per inning from the visiting team
    """
    inning_plays = defaultdict(list)
    for play in get_plays(game, include_home_team=include_home_team, include_visiting_team=include_visiting_team):
        inning_plays[play.inning].append(play)
    return dict(inning_plays)
