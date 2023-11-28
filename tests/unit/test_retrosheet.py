import pytest
from requests.exceptions import HTTPError

from pyretrosheet import retrosheet

MODULE_PATH = "pyretrosheet.retrosheet"


class TestRetrosheetClient:
    def test_get_zip_archive_of_years_play_by_play_data__happy_path(self, mocker, requests_mock):
        mocker.patch(f"{MODULE_PATH}.ZipFile")
        year = 2023
        client = retrosheet.RetrosheetClient()
        url = f"https://www.retrosheet.org/events/{year}eve.zip"
        request = requests_mock.get(url)

        client.get_zip_archive_of_years_play_by_play_data(year)

        assert request.call_count == 1

    def test_get_zip_archive_of_years_play_by_play_data__raises_on_status(self, requests_mock):
        year = 2023
        client = retrosheet.RetrosheetClient()
        url = f"https://www.retrosheet.org/events/{year}eve.zip"
        requests_mock.register_uri("GET", url, status_code=404)

        with pytest.raises(HTTPError):
            client.get_zip_archive_of_years_play_by_play_data(year)


def test_retrieve_years_play_by_play_files__no_download(mocker, tmp_path):
    client = retrosheet.RetrosheetClient()
    get_zip_archive_spy = mocker.spy(client, "get_zip_archive_of_years_play_by_play_data")
    year = 2023
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    evn_data_file = data_dir / f"{year}TEAM.EVN"
    evn_data_file.touch()
    eva_data_file = data_dir / f"{year}TEAM.EVA"
    eva_data_file.touch()

    data_files = retrosheet.retrieve_years_play_by_play_files(
        retrosheet_client=client,
        year=year,
        data_dir=data_dir,
    )

    assert data_files == [evn_data_file, eva_data_file]
    assert get_zip_archive_spy.call_count == 0


def test_retrieve_years_play_by_play_files__downloads_if_no_data_files(mocker, tmp_path):
    data_zip_archive = mocker.Mock()
    client = mocker.Mock()
    client.get_zip_archive_of_years_play_by_play_data.return_value = data_zip_archive
    extract_zip_archive = mocker.patch(f"{MODULE_PATH}._extract_zip_archive")
    yield_years_play_by_play_files = mocker.patch(f"{MODULE_PATH}._yield_years_play_by_play_files")

    year = 2023
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    data_files = retrosheet.retrieve_years_play_by_play_files(
        retrosheet_client=client,
        year=year,
        data_dir=data_dir,
    )

    assert extract_zip_archive.called_once_with(data_zip_archive, data_dir)
    assert data_files == list(yield_years_play_by_play_files.return_value)
