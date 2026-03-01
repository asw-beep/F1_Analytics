import pandas as pd


def add_driver_form(df, window=5):

    df = df.sort_values(["driverId", "date"])

    df["driver_form"] = (
        df.groupby("driverId")["finish_position"]
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    return df


def add_constructor_form(df, window=5):

    df = df.sort_values(["constructorId", "date"])

    df["constructor_form"] = (
        df.groupby("constructorId")["finish_position"]
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    return df


def add_driver_consistency(df, window=5):

    df = df.sort_values(["driverId", "date"])

    df["driver_consistency"] = (
        df.groupby("driverId")["finish_position"]
        .rolling(window, min_periods=2)
        .std()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    return df


def add_grid_advantage(df):

    df["grid_advantage"] = df["driver_form"] - df["grid_position"]

    return df


def main():

    df = pd.read_csv("data/processed/eda_dataset.csv")

    df = add_driver_form(df)
    df = add_constructor_form(df)
    df = add_driver_consistency(df)
    df = add_grid_advantage(df)

    df.to_csv("data/processed/featured_dataset.csv", index=False)

    print("\nFeature engineering complete.\n")

    print("Columns created:")
    print([
        "driver_form",
        "constructor_form",
        "driver_consistency",
        "grid_advantage"
    ])

    print("\nDataset shape:", df.shape)


if __name__ == "__main__":
    main()