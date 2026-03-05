import pandas as pd
import joblib
import os

from api_handler import get_latest_race_dataframe, get_latest_qualifying_dataframe
from feature_pipeline import build_features
from live_data import get_latest_completed_race


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_f1_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "featured_dataset.csv")



def predict_next_race():

    # load historical dataset
    historical_df = pd.read_csv(DATA_PATH)

    # fetch latest race
    live_df = get_latest_qualifying_dataframe()
    live_df["finish_position"] = None

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