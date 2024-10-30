import os
import json
import pytest
import requests
from unittest import mock
from project import load_config, setup_config, fetch_top_albums, export_data

# Mock configuration data
mock_config = {
    "lastfm_api_key": "mock_api_key",
    "lastfm_username": "mock_username",
    "export_format": "CSV",
    "export_location": "./mock_exports"
}

# Mock data to simulate Last.fm API response
mock_album_data = [
    {"name": "Album1", "artist": {"name": "Artist1"}, "playcount": "100"},
    {"name": "Album2", "artist": {"name": "Artist2"}, "playcount": "200"},
]

@pytest.fixture
def mock_requests_get():
    """Fixture to mock requests.get for Last.fm API calls."""
    with mock.patch('requests.get') as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"topalbums": {"album": mock_album_data}}
        mock_get.return_value = mock_response
        yield mock_get

def test_load_config(monkeypatch):
    """Test loading configuration from a file."""
    # Mock the open function to simulate reading from a config file
    with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(mock_config))):
        # Mock inputs in case setup_config gets called
        monkeypatch.setattr("builtins.input", lambda prompt: {
            "Enter your Last.fm API key: ": "mock_api_key",
            "Enter your Last.fm username: ": "mock_username",
            "Choose export format (CSV/JSON): ": "CSV",
            "Enter export directory (default is ./exports): ": "./mock_exports"
        }[prompt])

        config = load_config()
        assert config["lastfm_api_key"] == "mock_api_key"
        assert config["lastfm_username"] == "mock_username"
        assert config["export_format"] == "CSV"
        assert config["export_location"] == "./mock_exports"

def test_setup_config(monkeypatch):
    """Test setting up a new configuration and saving it to a file."""
    # Mock user input
    monkeypatch.setattr("builtins.input", lambda prompt: {
        "Enter your Last.fm API key: ": "mock_api_key",
        "Enter your Last.fm username: ": "mock_username",
        "Choose export format (CSV/JSON): ": "CSV",
        "Enter export directory (default is ./exports): ": "./mock_exports"
    }[prompt])

    # Mock open function to test writing to config file
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        config = setup_config()
        assert config["lastfm_api_key"] == "mock_api_key"
        assert config["lastfm_username"] == "mock_username"
        assert config["export_format"] == "CSV"
        assert config["export_location"] == "./mock_exports"
        mock_file().write.assert_called()

def test_fetch_top_albums(mock_requests_get):
    """Test fetching top albums from Last.fm."""
    albums = fetch_top_albums("mock_api_key", "mock_username")
    assert len(albums) == 2
    assert albums[0]["name"] == "Album1"
    assert albums[0]["artist"]["name"] == "Artist1"
    assert albums[0]["playcount"] == "100"

def test_export_data_csv(monkeypatch):
    """Test exporting data to a CSV file."""
    # Mock os.makedirs to avoid creating directories
    with mock.patch("os.makedirs") as mock_makedirs:
        # Mock open to avoid creating a real file
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            export_data(mock_album_data, mock_config)
            mock_makedirs.assert_called_with(mock_config["export_location"], exist_ok=True)
            mock_file.assert_called_once_with(os.path.join(mock_config["export_location"], "top_albums.csv"), 'w', newline='', encoding='utf-8')
            # Write header and data rows to the CSV
            mock_file().write.assert_any_call("Album Name,Artist,Playcount\r\n")
            mock_file().write.assert_any_call("Album1,Artist1,100\r\n")
            mock_file().write.assert_any_call("Album2,Artist2,200\r\n")

def test_export_data_json(monkeypatch):
    """Test exporting data to a JSON file."""
    mock_config_json = mock_config.copy()
    mock_config_json["export_format"] = "JSON"

    with mock.patch("os.makedirs") as mock_makedirs:
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            export_data(mock_album_data, mock_config_json)
            mock_makedirs.assert_called_with(mock_config["export_location"], exist_ok=True)
            mock_file.assert_called_once_with(os.path.join(mock_config["export_location"], "top_albums.json"), 'w', encoding='utf-8')
            # Check if json.dump was called with the correct data
            mock_file().write.assert_called()
