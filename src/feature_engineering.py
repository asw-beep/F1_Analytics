import pandas as pd
from feature_pipeline import build_features


def main():

    df = pd.read_csv("data/processed/eda_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])

    df = build_features(df)

    df.to_csv("data/processed/featured_dataset.csv", index=False)

    print("Feature pipeline complete.")
    print("Dataset shape:", df.shape)


if __name__ == "__main__":
    main()