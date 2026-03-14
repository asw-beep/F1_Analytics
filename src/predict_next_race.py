import pandas as pd
import joblib
import os
from datetime import datetime

from fastf1_handler import (
    get_latest_race_dataframe,
    get_latest_qualifying_dataframe,
    get_latest_qualifying,
    get_next_race,
    qualifying_to_dataframe
)
from feature_pipeline import build_features
from live_data import get_latest_completed_race


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_f1_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "featured_dataset.csv")


def get_next_race_info():
    """Get info about the next upcoming race (after the latest completed one)"""
    try:
        return get_next_race()
    except Exception as e:
        print(f"Error finding next race: {e}")

    return None


def map_fastf1_to_historical(live_df, historical_df):
    """
    Map FastF1 driver/constructor names to historical numeric IDs.
    Creates a mapping based on driver_name and constructor_name.
    """
    # Create lookup tables from historical data
    driver_name_to_id = historical_df.groupby("driver_name")["driverId"].first().to_dict()
    constructor_name_to_id = historical_df.groupby("constructor_name")["constructorId"].first().to_dict()
    
    # Map driverId from driver_name
    live_df["driverId"] = live_df.apply(
        lambda row: driver_name_to_id.get(row["driver_name"], row.get("driverId", row.get("DriverNumber"))),
        axis=1
    )
    
    # Map constructorId from constructor_name
    live_df["constructorId"] = live_df.apply(
        lambda row: constructor_name_to_id.get(row["constructor_name"], row.get("constructorId", row.get("TeamName"))),
        axis=1
    )
    
    # Ensure grid_position column exists
    if "grid_position" not in live_df.columns and "grid" in live_df.columns:
        live_df["grid_position"] = live_df["grid"]
    
    # Ensure driver_name column exists
    if "driver_name" not in live_df.columns and "BroadcastName" in live_df.columns:
        live_df["driver_name"] = live_df["BroadcastName"]
    
    # Ensure constructor_name column exists
    if "constructor_name" not in live_df.columns and "TeamName" in live_df.columns:
        live_df["constructor_name"] = live_df["TeamName"]
    
    return live_df


def predict_next_race():
    """
    Predict current race:
    - Use latest completed qualifying (most recent drivers' grid positions)
    - Display current/latest race info
    """

    # load historical dataset
    historical_df = pd.read_csv(DATA_PATH)

    # IMPORTANT: Get latest COMPLETED qualifying (e.g., Chinese GP)
    # This has the actual drivers and their current grid positions
    try:
        latest_qual = get_latest_qualifying()
        if latest_qual:
            live_df = qualifying_to_dataframe(latest_qual)
        else:
            live_df = pd.DataFrame()
    except Exception as e:
        print(f"Error getting qualifying: {e}")
        live_df = pd.DataFrame()

    if live_df.empty:
        return pd.DataFrame()

    # Map FastF1 names to historical IDs
    live_df = map_fastf1_to_historical(live_df, historical_df)

    # Keep the current race info from qualifying (don't overwrite with next race)
    # The race_name and date are already set from the latest qualifying

    live_df["finish_position"] = None

    # Select only columns that exist in historical data
    common_cols = [col for col in historical_df.columns if col in live_df.columns]
    live_df = live_df[common_cols]

    # combine
    df = pd.concat([historical_df, live_df], ignore_index=True)

    df["date"] = pd.to_datetime(df["date"])

    # rebuild features
    df = build_features(df)

    # take latest race
    latest_race = df[df["date"] == df["date"].max()].copy()

    features = [
        "grid_position",
        "driver_form",
        "constructor_form",
        "driver_consistency",
        "grid_advantage",
        "driver_circuit_avg_finish",
        "constructor_season_avg_finish"
    ]

    X = latest_race[features]

    # load model
    model = joblib.load(MODEL_PATH)

    probs = model.predict_proba(X)[:,1]
    probs = probs / probs.sum()
    latest_race["win_probability"] = probs

    leaderboard = latest_race.sort_values(
        "win_probability",
        ascending=False
    )

    # Build human-readable display names for drivers and constructors
    if "driver_name" in leaderboard.columns:
        leaderboard["driver_display"] = leaderboard["driver_name"].fillna("")
    else:
        leaderboard["driver_display"] = ""

    missing_driver_mask = leaderboard["driver_display"].eq("")
    leaderboard.loc[missing_driver_mask, "driver_display"] = (
        leaderboard.loc[missing_driver_mask, "driverId"]
        .astype(str)
        .str.replace("_", " ")
        .str.title()
    )

    if "constructor_name" in leaderboard.columns:
        leaderboard["constructor_display"] = leaderboard["constructor_name"].fillna("")
    else:
        leaderboard["constructor_display"] = ""

    missing_ctor_mask = leaderboard["constructor_display"].eq("")
    leaderboard.loc[missing_ctor_mask, "constructor_display"] = (
        leaderboard.loc[missing_ctor_mask, "constructorId"]
        .astype(str)
        .str.replace("_", " ")
        .str.title()
    )

    return leaderboard[[
        "year",
        "race_name",
        "date",
        "driverId",
        "constructorId",
        "driver_display",
        "constructor_display",
        "grid_position",
        "win_probability"
    ]]

if __name__ == "__main__":
    print(predict_next_race().head(10))