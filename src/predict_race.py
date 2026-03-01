import pandas as pd
import joblib

MODEL_PATH = "models/xgboost_f1_model.pkl"
DATA_PATH = "data/processed/featured_dataset.csv"


def load_model():
    return joblib.load(MODEL_PATH)


def load_data():
    return pd.read_csv(DATA_PATH)


def get_latest_race(df):

    df["date"] = pd.to_datetime(df["date"])

    latest_date = df["date"].max()

    latest_race = df[df["date"] == latest_date]

    return latest_race


def predict_race_leaderboard():

    model = load_model()

    df = load_data()

    race_df = get_latest_race(df)

    features = [
        "grid_position",
        "driver_form",
        "constructor_form",
        "driver_consistency",
        "grid_advantage"
    ]

    race_df = race_df.dropna(subset=features)

    X = race_df[features]

    probs = model.predict_proba(X)[:, 1]

    race_df["win_probability"] = probs

    leaderboard = race_df.sort_values(
        "win_probability",
        ascending=False
    )

    return leaderboard[[
        "driver_name",
        "constructor_name",
        "grid_position",
        "win_probability"
    ]]


if __name__ == "__main__":

    leaderboard = predict_race_leaderboard()

    print("\nPredicted Race Leaderboard:\n")

    print(leaderboard.head(10))