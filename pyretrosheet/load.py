"""Load raw Retrosheet data into models."""

from collections.abc import Iterator
from copy import deepcopy
from pathlib import Path

from pyretrosheet.models.game import Game
from pyretrosheet.retrosheet import RetrosheetClient, retrieve_years_play_by_play_files


def yield_games_in_year(retrosheet_client: RetrosheetClient, data_dir: Path, year: int) -> Iterator[Game]:
    """Yield games for a given year.

    Args:
        retrosheet_client: A RetrosheetClient
        data_dir: dir where data is located
        year: the year to load data from
    """
    for file in retrieve_years_play_by_play_files(
        retrosheet_client=retrosheet_client,
        year=year,
        data_dir=data_dir,
    ):
        for games_lines in _yield_game_lines(file.read_text().splitlines()):
            yield Game.from_retrosheet_game_lines(games_lines)


def _yield_game_lines(lines: list[str]) -> Iterator[list[str]]:
    """Yield the lines corresponding to each game in a Retrosheet play-by-play file.

    Args:
        lines: lines of a play-by-play file (includes multiple games in a single file)
    """
    current_game_lines: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("id,") and current_game_lines:
            yield deepcopy(current_game_lines)
            current_game_lines.clear()

        current_game_lines.append(line)

    if current_game_lines:
        yield deepcopy(current_game_lines)
