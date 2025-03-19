import re
from datetime import date, datetime, timedelta


def get_league_icon(league: str):
    if league == "Wood":
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/wood.b8940cb5.svg"
    elif league == "Stone":
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/stone.3434a62c.svg"
    elif league == "Bronze":
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/bronze.b529d5c1.svg"
    elif league == "Silver":
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/silver.6e7fa8dc.svg"
    elif league == "Crystal":
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/crystal.232d0aa5.svg"
    elif league == "Elite":
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/elite.970af95e.svg"
    elif league == "Champion":
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/champion.0c764ca5.svg"
    elif league == "Legend":
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/legend.1ea014f3.svg"
    else:
        icon = "https://www.chess.com/bundles/web/images/leagues/badges/wood.b8940cb5.svg"
    return icon


def format_last_connection(last_seen: datetime) -> str:
    today = date.today()
    yesterday = today - timedelta(days=1)

    if last_seen.date() == today:
        nb_hours = hours_since_last_connection(last_seen)
        if nb_hours == 0:
            return "En ligne"
        elif nb_hours == 1:
            return f"Il y a {nb_hours} heure"
        else:
            return f"Il y a {nb_hours} heures"
    elif last_seen.date() == yesterday:
        return "Hier"
    else:
        delta_days = (today - last_seen.date()).days
        return f"Il y a {delta_days} jours"


def hours_since_last_connection(last_seen: datetime) -> int:
    now = datetime.now()
    time_difference = now - last_seen
    hours_difference = time_difference.total_seconds() // 3600
    return int(hours_difference)


def get_total_games_played(player_stats: dict):
    total_games = 0
    for _, value in player_stats.items():
        if isinstance(value, dict) and "record" in value:
            record = value["record"]
            games_in_gamemode = record.get("win", 0) + record.get("loss", 0) + record.get("draw", 0)
            total_games += games_in_gamemode
    return total_games


def format_games_played(player_stats: dict) -> str:
    total_games = get_total_games_played(player_stats)
    if total_games == 0:
        return "Aucune partie jouée"
    elif total_games == 1:
        return "1 partie jouée"
    else:
        return f"{total_games} parties jouées"


def format_friends(player_info: dict) -> str:
    friends = player_info.get("followers")
    if friends == 0:
        return "Aucun ami"
    elif friends == 1:
        return "1 ami"
    else:
        return f"{friends} amis"


def get_game_outcome(username: str, game: dict):
    white = game.get("white")
    black = game.get("black")
    if white.get("username") == username:
        if white.get("result") == "win":
            winner = "white"
            outcome = "Victoire"
        elif black.get("result") == "win":
            winner = "black"
            outcome = "Défaite"
        else:
            winner = None
            outcome = "Match nul"
    else:
        if white.get("result") == "win":
            winner = "white"
            outcome = "Défaite"
        elif black.get("result") == "win":
            winner = "black"
            outcome = "Victoire"
        else:
            winner = None
            outcome = "draw"

    if outcome == "Victoire":
        card_color = "green"
    elif outcome == "Défaite":
        card_color = "red"
    else:
        card_color = "gray"

    return outcome, winner, card_color


def format_accuracy(game: dict):
    accuracies = game.get("accuracies")
    if accuracies:
        white_accuracy = accuracies.get("white")
        black_accuracy = accuracies.get("black")
        accuracy_status = "found"
    else:
        white_accuracy = None
        black_accuracy = None
        accuracy_status = "not found"
    return white_accuracy, black_accuracy, accuracy_status


def get_number_of_moves(game):
    pgn = game.get("pgn", "")
    # Recherche le dernier numéro de coup joué (ex: 26. dans "26... Qe2#")
    moves = re.findall(r"\b\d+\. ", pgn)
    nb_moves = moves[-1]
    nb_moves = nb_moves.replace(". ", "")
    return int(nb_moves) if nb_moves else 0  # Supprime le "." et convertit en int


def get_outcome_icon(game):
    white = game.get("white")
    black = game.get("black")

    #
    # Checkmated
    if white.get("result") == "checkmated":
        loser = "white"
        icon = "checkmate_white"
        msg = "Les blancs ont perdu par échec et mat"
    elif black.get("result") == "checkmated":
        loser = "black"
        icon = "checkmate_black"
        msg = "Les noirs ont perdu par échec et mat"

    #
    # Resigned
    elif any([white.get("result") == "resigned", white.get("result") == "abandoned"]):
        loser = "white"
        icon = "resign_white"
        msg = "Les blancs ont abandonné"
    elif any([black.get("result") == "resigned", black.get("result") == "abandoned"]):
        loser = "black"
        icon = "resign_black"
        msg = "Les noirs ont abandonné"

    #
    # Timeout
    elif white.get("result") == "timeout":
        loser = "white"
        icon = "unnamed_clock_white"
        msg = "Les blancs ont perdu au temps"
    elif black.get("result") == "timeout":
        loser = "black"
        icon = "unnamed_clock_black"
        msg = "Les noirs ont perdu au temps"

    #
    # Threecheck
    elif white.get("result") == "threecheck":
        loser = "white"
        icon = "checkmate_white"
        msg = "Les blancs ont perdu : Règle des 3 échecs"
    elif black.get("result") == "threecheck":
        loser = "black"
        icon = "checkmate_black"
        msg = "Les noirs ont perdu : Règle des 3 échecs"

    #
    # King of the hill
    elif white.get("result") == "kingofthehill":
        loser = "white"
        icon = "checkmate_white"
        msg = "Les blancs ont perdu : Le roi adversaire a atteint la colline"
    elif black.get("result") == "kingofthehill":
        loser = "black"
        icon = "checkmate_black"
        msg = "Les noirs ont perdu : Le roi adversaire a atteint la colline"

    #
    # Draw
    else:
        loser = None
        icon = "draw_white"
        if any([white.get("result") == "stalemate", black.get("result") == "stalemate"]):
            msg = "Match nul : Pat"
        if any([white.get("result") == "agreed", black.get("result") == "agreed"]):
            msg = "Match nul : Accord commun"
        if any([white.get("result") == "repetition", black.get("result") == "repetition"]):
            msg = "Match nul : Répétition"
        if any([white.get("result") == "50move", black.get("result") == "50move"]):
            msg = "Match nul : Règle des 50 coups"
        if any([white.get("result") == "timevsinsufficient", black.get("result") == "timevsinsufficient"]):
            msg = "Match nul : Temps contre matériel insuffisant"
        else:
            icon = "mistake"
            msg = "Fin de partie inconnue"

    return loser, icon, msg
