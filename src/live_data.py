import pandas as pd
from datetime import datetime
from fastf1_handler import get_latest_race_dataframe


def get_latest_completed_race():
    """Get the latest completed race results using FastF1"""
    return get_latest_race_dataframe()
