import pandas as pd
from pathlib import Path

DATA_DIR = Path("../data/raw/archive(1)")

def load_data():
    races = pd.read_csv(DATA_DIR / "races.csv")
    results = pd.read_csv(DATA_DIR / "results.csv")
    drivers = pd.read_csv(DATA_DIR / "drivers.csv")
    constructors = pd.read_csv(DATA_DIR / "constructors.csv")
    qualifying = pd.read_csv(DATA_DIR / "qualifying.csv")

    return {
        "races": races,
        "results": results,
        "drivers": drivers,
        "constructors": constructors,
        "qualifying": qualifying
    }