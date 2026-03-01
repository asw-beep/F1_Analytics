import pandas as pd

DATA_PATH = "../data/processed/featured_dataset.csv"


def load_featured_data():
    df = pd.read_csv(DATA_PATH)
    return df


def get_latest_driver_features(driver_name):

    df = load_featured_data()

    driver_df = df[df["driver_name"] == driver_name]

    if driver_df.empty:
        raise ValueError(f"No data found for driver: {driver_name}")

    driver_df = driver_df.sort_values("date", ascending=False)

    latest = driver_df.iloc[0]

    features = {
        "grid_position": int(latest["grid_position"]),
        "driver_form": float(latest["driver_form"]),
        "constructor_form": float(latest["constructor_form"]),
        "driver_consistency": float(latest["driver_consistency"]),
        "grid_advantage": float(latest["grid_advantage"])
    }

    return features


def get_all_drivers():

    df = load_featured_data()

    drivers = sorted(df["driver_name"].dropna().unique())

    return drivers