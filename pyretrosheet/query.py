"""Query data from different views (team, game, seasonal, etc.)."""
from dataclasses import dataclass
from pathlib import Path

from pyretrosheet.models.game import Game


@dataclass
class Query:
    """Interface with data using various queries.

    Args:
        data_dir: the dir where Retrosheet data is stored
    """

    data_dir: Path

    def get_games_in_year(self, year: int) -> None:
        """Load data for a specific year/season.

        Args:
            year: the year to load data for
        """
        raise NotImplementedError()
