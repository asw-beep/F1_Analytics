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


def add_driver_circuit_performance(df):

    df = df.sort_values(["driverId", "circuitId", "date"])

    df["driver_circuit_avg_finish"] = (
        df.groupby(["driverId", "circuitId"])["finish_position"]
        .expanding()
        .mean()
        .shift(1)
        .reset_index(level=[0,1], drop=True)
    )

    return df


def add_constructor_season_dominance(df):

    df = df.sort_values(["constructorId", "year", "date"])

    df["constructor_season_avg_finish"] = (
        df.groupby(["constructorId", "year"])["finish_position"]
        .expanding()
        .mean()
        .shift(1)
        .reset_index(level=[0,1], drop=True)
    )

    return df


def add_grid_advantage(df):
    df["grid_advantage"] = df["driver_form"] - df["grid_position"]
    return df


def build_features(df):

    df = add_driver_form(df)
    df = add_constructor_form(df)
    df = add_driver_consistency(df)
    df = add_driver_circuit_performance(df)
    df = add_constructor_season_dominance(df)
    df = add_grid_advantage(df)

    return df