"""Retrieve, load, and persist retrosheet.org data."""
from collections.abc import Iterator
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from requests import Session


@dataclass
class RetrosheetClient:
    """retrosheet.org client to retrieve Retrosheet data files.

    Data files: https://www.retrosheet.org/game.htm

    Args:
        base_url: the URL base for the client

    Attributes:
        base_url: the URL base for the client
        _session: internal requests session
    """

    base_url: str = "https://www.retrosheet.org"
    _session: Session = field(init=False)

    def __post_init__(self):
        """Initialize the requests session."""
        self._session = Session()

    def get_zip_archive_of_years_play_by_play_data(self, year: int) -> ZipFile:
        """Get the zip archive of a year's play-by-play data.

        Args:
            year: the year to retrieve play-by-play data for.
        """
        response = self._session.get(f"{self.base_url}/events/{year}eve.zip")
        response.raise_for_status()
        return ZipFile(BytesIO(response.content))


def retrieve_years_play_by_play_files(
    year: int,
    data_dir: Path,
    retrosheet_client: RetrosheetClient | None = None,
    force_download: bool = False,
) -> list[Path]:
    """Retrieve a year's play-by-play files.

    Args:
        year: the year to retrieve play-by-play files for
        data_dir: the dir to retrieve/store play-by-play files from/to
        retrosheet_client: a Retrosheet client
        force_download: do not use existing data and force a new download of the data
    """
    retrosheet_client = retrosheet_client or RetrosheetClient()
    data_files = list(_yield_years_play_by_play_files(data_dir, year))
    if data_files and not force_download:
        return data_files

    data_zip_archive = retrosheet_client.get_zip_archive_of_years_play_by_play_data(year)
    _extract_zip_archive(data_zip_archive, data_dir)
    return list(_yield_years_play_by_play_files(data_dir, year))


def _extract_zip_archive(zip_archive: ZipFile, target_dir: Path) -> None:
    """Extract a zip archive to a target directory.

    If the target directory does not exist, it and its parents will be created.

    Args:
        zip_archive: the zip file to extract
        target_dir: the path of the directory to extract to
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    zip_archive.extractall(target_dir.as_posix())


def _yield_years_play_by_play_files(data_dir: Path, year: int) -> Iterator[Path]:
    """Yield a year's play-by-play files.

    Args:
        data_dir: the directory to yield the files from
        year: the year to retrieve files for
    """
    yield from data_dir.glob(f"{year}*.EVN")  # National League data files
    yield from data_dir.glob(f"{year}*.EVA")  # American League data files
    yield from data_dir.glob(f"{year}*.EVF")  # Federal League data files
    yield from data_dir.glob(f"{year}*.EVR")  # Negro League data files
