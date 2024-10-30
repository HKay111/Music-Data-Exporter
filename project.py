import os
import json
import requests
import csv

CONFIG_FILE = 'config.json'

def load_config():
    """Load or create a configuration file with the user's Last.fm API details."""
    if not os.path.exists(CONFIG_FILE):
        return setup_config()

    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)

    # Ensure essential config fields are present
    if 'lastfm_api_key' not in config or 'lastfm_username' not in config:
        print("Configuration incomplete. Starting setup.")
        return setup_config()

    return config

def setup_config():
    """Guide the user through setting up their API key and saving it to a config file."""
    config = {
        "lastfm_api_key": input("Enter your Last.fm API key: "),
        "lastfm_username": input("Enter your Last.fm username: "),
        "export_format": input("Choose export format (CSV/JSON): ").upper(),
        "export_location": input("Enter export directory (default is ./exports): ") or "./exports"
    }

    # Save configuration to the file
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

    print("Configuration saved. You're all set!")
    return config

def fetch_top_albums(api_key, username):
    """Fetch top albums from Last.fm using the user's API key and username."""
    url = 'https://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.getTopAlbums',
        'user': username,
        'api_key': api_key,
        'format': 'json',
        'limit': 10  
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('topalbums', {}).get('album', [])
    else:
        print("Failed to fetch data from Last.fm. Check your API key or username.")
        return []

def export_data(albums, config):
    """Export album data to CSV or JSON in the specified location."""
    export_location = config['export_location']
    export_format = config['export_format']

    # Ensure export directory exists
    os.makedirs(export_location, exist_ok=True)

    if export_format == "CSV":
        filepath = os.path.join(export_location, "top_albums.csv")
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Album Name", "Artist", "Playcount"])
            for album in albums:
                writer.writerow([album.get('name', 'Unknown Album'),
                                 album.get('artist', {}).get('name', 'Unknown Artist'),
                                 album.get('playcount', '0')])
        print(f"Data exported successfully to {filepath}")

    elif export_format == "JSON":
        filepath = os.path.join(export_location, "top_albums.json")
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(albums, jsonfile, indent=4)
        print(f"Data exported successfully to {filepath}")

    else:
        print("Invalid export format specified in configuration.")

def main():
    """Main function to load configuration, fetch top albums, and export them."""
    config = load_config()

    albums = fetch_top_albums(config['lastfm_api_key'], config['lastfm_username'])

    if albums:
        print(f"Found {len(albums)} top albums:")
        for album in albums:
            album_name = album.get('name', 'Unknown Album')
            artist_name = album.get('artist', {}).get('name', 'Unknown Artist')
            playcount = album.get('playcount', '0')
            print(f"{album_name} by {artist_name} (Plays: {playcount})")

        export_data(albums, config)
    else:
        print("No albums found.")


if __name__ == '__main__':
    main()

# bd6bebcb115de097e3d178af158f3cb5
# HKay01
