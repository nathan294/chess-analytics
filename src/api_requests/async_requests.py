import asyncio
from datetime import date

import httpx

HEADERS = {"User-Agent": "PostmanRuntime/7.29.0"}


async def fetch_player_archives(client: httpx.AsyncClient, player_name: str):
    """Fetch player archives from Chess.com API."""
    url = f"https://api.chess.com/pub/player/{player_name}/games/archives"
    try:
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()  # Raise an exception for HTTP errors
    except httpx.HTTPStatusError as e:
        print(f"Error fetching archives for {player_name}: {e}")
        return None


async def fetch_player_games(client: httpx.AsyncClient, archive: str):
    """Fetch latest games from the most recent archive."""
    try:
        response = await client.get(archive, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("games", [])[::-1]  # Reverse to get latest games first
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()  # Raise an exception for HTTP errors
    except httpx.HTTPStatusError as e:
        print(f"Error fetching games: {e}")
        return None


async def fetch_player_base_information(client: httpx.AsyncClient, player_name: str):
    """Fetch player's base information."""
    url = f"https://api.chess.com/pub/player/{player_name}"
    try:
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()  # Raise an exception for HTTP errors
    except httpx.HTTPStatusError as e:
        print(f"Error fetching base info for {player_name}: {e}")
        return None


async def fetch_player_stats(client: httpx.AsyncClient, player_name: str):
    """Fetch player's stats."""
    url = f"https://api.chess.com/pub/player/{player_name}/stats"
    try:
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()  # Raise an exception for HTTP errors
    except httpx.HTTPStatusError as e:
        print(f"Error fetching stats for {player_name}: {e}")
        return None


async def fetch_player_data(player_name: str):
    """Fetch all player-related data concurrently."""
    player_name = player_name.lower()  # Ensure username is lowercase

    async with httpx.AsyncClient() as client:
        player_archives = await fetch_player_archives(client, player_name)

        if not player_archives or "archives" not in player_archives:
            print(f"No archives found for {player_name}.")
            return None, None, None, None

        if len(player_archives.get("archives")) > 0:
            latest_archive = player_archives.get("archives")[-1]  # Get the latest archive URL
        else:
            today = date.today()
            latest_archive = f"https://api.chess.com/pub/player/{player_name}/games/{today.year}/{str(today.month).zfill(2)}"

        player_info, player_stats, player_recent_games = await asyncio.gather(
            fetch_player_base_information(client, player_name),
            fetch_player_stats(client, player_name),
            fetch_player_games(client, latest_archive),
        )

        return player_info, player_stats, player_recent_games, player_archives


async def fetch_all_archives(player_archives: dict):
    async with httpx.AsyncClient() as client:
        tasks = [fetch_player_games(client, archive) for archive in player_archives.get("archives", [])]
        results = await asyncio.gather(*tasks)
        # Flatten the list of lists into a single list
        all_games = [game for sublist in results for game in sublist]
        return all_games
