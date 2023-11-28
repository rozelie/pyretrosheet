from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / "data"


def get_game_lines() -> str:
    file = TEST_DATA_DIR / "game_lines.txt"
    return file.read_text()
