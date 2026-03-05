import pandas as pd
import joblib
import os

from live_data import get_latest_completed_race
from feature_pipeline import build_features


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_f1_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "featured_dataset.csv")


def predict_next_race():

    # load historical dataset
    historical_df = pd.read_csv(DATA_PATH)

    # fetch latest race
    live_df = get_latest_completed_race()

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

    latest_race["win_probability"] = probs

    leaderboard = latest_race.sort_values(
        "win_probability",
        ascending=False
    )

    return leaderboard[[
        "year",
        "race_name",
        "date",
        "driverId",
        "constructorId",
        "grid_position",
        "win_probability"
    ]]

if __name__ == "__main__":
    print(predict_next_race().head(10))