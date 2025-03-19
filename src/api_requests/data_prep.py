from datetime import date, datetime, timedelta
from typing import Literal

import polars as pl


def get_games_dataframe(player_name: str, all_player_games: list):
    df_raw = pl.json_normalize(all_player_games, separator="_")

    df = df_raw.with_columns(
        # Create "player_name" column
        pl.lit(player_name).str.to_lowercase().alias("player_name")
    )
    df = df.with_columns(
        #
        # Create "player_outcome" column
        pl.when(pl.col("black_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("black_result"))
        .when(pl.col("white_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("white_result"))
        .otherwise(None)
        .alias("player_outcome"),
    )
    df = df.select(
        # player_name
        pl.col("player_name"),
        #
        # Format end_time date
        pl.col("end_time").map_elements(lambda x: datetime.fromtimestamp(x), return_dtype=datetime).alias("end_time"),
        # Get "time_class"
        pl.col("time_class"),
        # Get "rules"
        pl.col("rules"),
        # Create "gamemode" column
        (pl.col("time_class") + "_" + pl.col("rules")).alias("gamemode"),
        #
        # Create "player_side" column
        pl.when(pl.col("black_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.lit("black"))
        .when(pl.col("white_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.lit("white"))
        .otherwise(None)
        .alias("player_side"),
        # player_outcome
        pl.col("player_outcome"),
        #
        # Create "opponent_outcome" column
        pl.when(pl.col("black_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("white_result"))
        .when(pl.col("white_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("black_result"))
        .otherwise(None)
        .alias("opponent_outcome"),
        #
        # Create "player_result" column
        pl.when(pl.col("player_outcome").is_in(["checkmated", "resigned", "abandoned", "timeout", "threecheck", "kingofthehill"]))
        .then(pl.lit("loss"))
        .when(pl.col("player_outcome") == "win")
        .then(pl.lit("win"))
        .otherwise(pl.lit("draw"))
        .alias("player_result"),
        #
        # Create "player_rating" column
        pl.when(pl.col("black_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("black_rating"))
        .when(pl.col("white_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("white_rating"))
        .otherwise(None)
        .alias("player_rating"),
        #
        # Create "opponent_rating" column
        pl.when(pl.col("black_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("white_rating"))
        .when(pl.col("white_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("black_rating"))
        .otherwise(None)
        .alias("opponent_rating"),
        #
        # Create "player_accuracy" column
        pl.when(pl.col("black_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("accuracies_black"))
        .when(pl.col("white_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("accuracies_white"))
        .otherwise(None)
        .alias("player_accuracy"),
        #
        # Create "opponent_accuracy" column
        pl.when(pl.col("black_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("accuracies_white"))
        .when(pl.col("white_username").str.to_lowercase() == pl.col("player_name"))
        .then(pl.col("accuracies_black"))
        .otherwise(None)
        .alias("opponent_accuracy"),
        #
        # Create "opening_name" column
        pl.col("eco").str.extract(r"/openings/([a-zA-Z-]+)").str.replace_all(r"-", " ").str.strip_chars_end(" ").alias("opening_name"),
        #
        # Create "opening_moves" column
        pl.col("eco").str.extract(r"(\d.*)").str.replace_all(r"-", " ").str.strip_chars_end(" ").alias("opening_moves"),
    ).sort(by=pl.col("end_time"), descending=True)

    return df


def filter_df_on_gamemode(df: pl.DataFrame, gamemode: str):
    return df.filter(pl.col("gamemode") == gamemode)


def filter_df_on_periodicity(
    df: pl.DataFrame, periodicity: Literal["tab-7days", "tab-30days", "tab-90days", "tab-1year", "tab-total"]
) -> pl.DataFrame:
    today = date.today()

    if periodicity == "tab-7days":
        df = df.filter(pl.col("end_time") >= today - timedelta(days=7))
    elif periodicity == "tab-30days":
        df = df.filter(pl.col("end_time") >= today - timedelta(days=30))
    elif periodicity == "tab-90days":
        df = df.filter(pl.col("end_time") >= today - timedelta(days=90))
    elif periodicity == "tab-1year":
        df = df.filter(pl.col("end_time") >= today - timedelta(days=365))
    elif periodicity == "tab-total":
        pass  # No filter needed, return full dataset

    return df


def get_ranking_evolution(df: pl.DataFrame):
    df = df.with_columns(pl.col("end_time").dt.date())
    df = df.group_by("end_time").first().select(pl.col("end_time"), pl.col("player_rating")).sort(by="end_time", descending=True)

    latest_ranking = df.select(pl.col("player_rating").first()).item()
    oldest_ranking = df.select(pl.col("player_rating").last()).item()

    if latest_ranking is None or oldest_ranking is None:
        return 0

    return latest_ranking - oldest_ranking
