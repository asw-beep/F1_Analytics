import fastf1
import pandas as pd
from datetime import datetime
import os

# Set cache directory relative to this file
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
fastf1.Cache.enable_cache(CACHE_DIR)


def get_current_season():
    """Get the current F1 season year"""
    return datetime.now().year


def get_race_schedule(year=None):
    """Get the race schedule for a given year using FastF1"""
    if year is None:
        year = get_current_season()
    
    schedule = fastf1.get_event_schedule(year)
    
    races = []
    for _, row in schedule.iterrows():
        races.append({
            "raceName": row["EventName"],
            "Circuit": {"circuitId": row["EventFormat"]},
            "date": str(row["EventDate"].date()) if pd.notna(row["EventDate"]) else None,
            "season": str(year),
            "round": row["RoundNumber"]
        })
    
    return races


def get_last_completed_race(year=None):
    """Get the last completed race using FastF1"""
    if year is None:
        year = get_current_season()
    
    schedule = fastf1.get_event_schedule(year)
    
    # Filter out races that haven't happened yet
    today = pd.Timestamp.now()
    completed_races = schedule[schedule["EventDate"] <= today]
    
    if completed_races.empty:
        # Try previous year
        return get_last_completed_race(year - 1)
    
    last_race = completed_races.iloc[-1]
    
    session = fastf1.get_session(year, last_race["EventName"], "R")
    session.load()
    
    results = session.results
    
    records = []
    for _, row in results.iterrows():
        if pd.notna(row["Position"]):
            records.append({
                "race_name": last_race["EventName"],
                "circuitId": last_race["EventFormat"],
                "date": str(last_race["EventDate"].date()),
                "year": year,
                "driverId": row["DriverNumber"],
                "constructorId": row["TeamName"],
                "grid_position": int(row["GridPosition"]) if pd.notna(row["GridPosition"]) else None,
                "finish_position": int(row["Position"]),
                "driver_name": row["BroadcastName"],
                "constructor_name": row["TeamName"]
            })
    
    return [records] if records else []


def get_latest_race_dataframe():
    """Get the latest race results as a DataFrame"""
    races = get_last_completed_race()
    
    if not races or not races[0]:
        return pd.DataFrame()
    
    return pd.DataFrame(races[0])


def get_latest_qualifying(year=None):
    """Get the latest qualifying results using FastF1"""
    if year is None:
        year = get_current_season()
    
    schedule = fastf1.get_event_schedule(year)
    
    # Filter out races that haven't happened yet
    today = pd.Timestamp.now()
    completed_races = schedule[schedule["EventDate"] <= today]
    
    if completed_races.empty:
        # Try previous year
        return get_latest_qualifying(year - 1)
    
    last_race = completed_races.iloc[-1]
    
    try:
        session = fastf1.get_session(year, last_race["EventName"], "Q")
        session.load()
        
        results = session.results
        
        records = []
        for _, row in results.iterrows():
            if pd.notna(row["Position"]):
                records.append({
                    "race_name": last_race["EventName"],
                    "circuitId": last_race["EventFormat"],
                    "date": str(last_race["EventDate"].date()),
                    "year": year,
                    "driverId": row["DriverNumber"],
                    "constructorId": row["TeamName"],
                    "grid_position": int(row["Position"]),
                    "driver_name": row["BroadcastName"],
                    "constructor_name": row["TeamName"]
                })
        
        return [records] if records else []
    except Exception:
        # Fallback to race session if qualifying not available
        return get_last_completed_race(year)


def get_latest_qualifying_dataframe():
    """Get the latest qualifying results as a DataFrame"""
    races = get_latest_qualifying()
    
    if not races or not races[0]:
        return pd.DataFrame()
    
    return pd.DataFrame(races[0])


def qualifying_to_dataframe(races):
    """Convert qualifying results to DataFrame"""
    if not races:
        return pd.DataFrame()
    
    # Handle nested list structure
    if isinstance(races[0], list):
        return pd.DataFrame(races[0])
    
    return pd.DataFrame(races)


def get_next_race(year=None):
    """Get the next upcoming race using FastF1"""
    if year is None:
        year = get_current_season()
    
    schedule = fastf1.get_event_schedule(year)
    
    today = pd.Timestamp.now()
    upcoming_races = schedule[schedule["EventDate"] > today]
    
    if upcoming_races.empty:
        # Try next year
        return get_next_race(year + 1)
    
    next_race = upcoming_races.iloc[0]
    
    return {
        "raceName": next_race["EventName"],
        "Circuit": {"circuitId": next_race["EventFormat"]},
        "date": str(next_race["EventDate"].date()),
        "season": str(year),
        "round": next_race["RoundNumber"]
    }
