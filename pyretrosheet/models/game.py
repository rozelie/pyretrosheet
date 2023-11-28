"""Encapsulates Retrosheet game data."""
from dataclasses import dataclass


@dataclass
class Game:
    """A game as defined in Retrosheet."""

    @classmethod
    def from_retrosheet_game_lines(cls, game_lines: list[str]) -> "Game":
        """Load a game from Retrosheet game lines.

        Args:
            game_lines: game lines from a Retrosheet game
        """
        raise NotImplementedError()
