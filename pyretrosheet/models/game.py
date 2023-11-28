"""Encapsulates Retrosheet game data."""
from dataclasses import dataclass

from pyretrosheet.models.game_id import GameID
from pyretrosheet.models.play import Play
from pyretrosheet.models.player import Player


@dataclass
class Game:
    """A game as defined in Retrosheet.

    Args:
        game_id: the game id
        info: miscellaneous encoded information like temperature, attendance, umpire names, etc.
        home_team_id: the Retrosheet team id of the home team
        visiting_team_id: the Retrosheet team id of the visiting team
        home_team_players: the players on the home team
        home_team_starting_lineup: the players of starting lineup on the home team
        visiting_team_players: the players on the visiting team
        visiting_team_starting_lineup: the players of starting lineup on the visiting team
        plays: the plays that occurred over the course of the game
        player_id_to_earned_runs: mapping of player id to earned runs
    """

    game_id: GameID
    info: dict[str, str]
    home_team_id: str
    visiting_team_id: str
    home_team_players: list[Player]
    home_team_starting_lineup: list[Player]
    visiting_team_players: list[Player]
    visiting_team_starting_lineup: list[Player]
    plays: list[Play]
    player_id_to_earned_runs: dict[str, int]

    @classmethod
    def from_retrosheet_game_lines(cls, game_lines: list[str]) -> "Game":
        """Load a game from Retrosheet game lines.

        Args:
            game_lines: game lines from a Retrosheet game
        """
        raise NotImplementedError()
