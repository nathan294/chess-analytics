import requests


def sync_fetch_player_base_information(player_name: str):
    url = f"https://api.chess.com/pub/player/{player_name}"
    headers = {"User-Agent": "PostmanRuntime/7.29.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def sync_fetch_player_stats(player_name: str):
    url = f"https://api.chess.com/pub/player/{player_name}/stats"
    headers = {"User-Agent": "PostmanRuntime/7.29.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def sync_fetch_player_archives(user_name: str):
    url = f"https://api.chess.com/pub/player/{user_name}/games/archives"
    headers = {"User-Agent": "PostmanRuntime/7.29.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def sync_fetch_player_games(archive: str):
    url = archive
    headers = {"User-Agent": "PostmanRuntime/7.29.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    games = response.json().get("games", [])
    return games[::-1]  # Return reversed list to have latest games first
