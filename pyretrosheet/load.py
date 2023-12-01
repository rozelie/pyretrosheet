"""Load raw Retrosheet data into models."""
from collections.abc import Iterator
from copy import deepcopy
from pathlib import Path

from pyretrosheet import retrosheet
from pyretrosheet.models.exceptions import ParseError
from pyretrosheet.models.game import Game

PYRETROSHEET_DIR = Path.home() / ".pyretrosheet"
DEFAULT_DATA_DIR = PYRETROSHEET_DIR / "data"


def load_games(year: int, data_dir: Path | str = DEFAULT_DATA_DIR, force_download: bool = False) -> Iterator[Game]:
    """Load Retrosheet games.

    Args:
        year: the year to load Retrosheet data for
        data_dir: dir where data will be stored (defaults to '~/.pyretrosheet/data')
        force_download: force a fresh download of the data even if it already exists
    """
    data_dir = data_dir if isinstance(data_dir, Path) else Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    for play_by_play_file in retrosheet.retrieve_years_play_by_play_files(
        year=year,
        data_dir=Path(data_dir) or DEFAULT_DATA_DIR,
        force_download=force_download,
    ):
        yield from _iter_games_from_play_by_play_file(play_by_play_file)


def _iter_games_from_play_by_play_file(file: Path) -> Iterator[Game]:
    """Iterate games loaded from a play by play file.

    Args:
        file: the file path to the play by play file
    """
    for games_lines in _iter_game_lines(file.read_text().splitlines()):
        try:
            yield Game.from_game_lines(games_lines)
        except ParseError as e:
            raise ParseError(e.looking_for_value, e.raw_value, e.game_line, file.as_posix()) from e


def _iter_game_lines(lines: list[str]) -> Iterator[list[str]]:
    """Iterate the lines corresponding to each game in a Retrosheet play-by-play file.

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
