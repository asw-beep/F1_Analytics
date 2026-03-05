import requests
import pandas as pd
from datetime import datetime


BASE_URL = "https://api.jolpi.ca/ergast/f1"


def fetch_json(endpoint):

    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"API request failed: {url}")

    return response.json()


# --------------------------------
# CURRENT SEASON
# --------------------------------

def get_current_season():

    return datetime.now().year


# --------------------------------
# RACE SCHEDULE
# --------------------------------

def get_race_schedule():

    data = fetch_json("current/races.json")

    return data["MRData"]["RaceTable"]["Races"]


# --------------------------------
# LAST COMPLETED RACE (ROBUST)
# --------------------------------

def get_last_completed_race():

    current_year = get_current_season()

    # try current season first
    data = fetch_json("current/last/results.json")

    races = data["MRData"]["RaceTable"]["Races"]

    if races:
        return races

    # fallback loop (previous seasons)
    for year in range(current_year - 1, 1950, -1):

        data = fetch_json(f"{year}/last/results.json")

        races = data["MRData"]["RaceTable"]["Races"]

        if races:
            return races

    raise Exception("No race results found in API.")


# --------------------------------
# RESULTS → DATAFRAME
# --------------------------------

def results_to_dataframe(races):

    records = []

    for race in races:

        race_name = race["raceName"]
        circuit = race["Circuit"]["circuitId"]
        date = race["date"]
        year = int(race["season"])

        for result in race["Results"]:

            driver = result["Driver"]
            constructor = result["Constructor"]

            records.append({

                "race_name": race_name,
                "circuitId": circuit,
                "date": date,
                "year": year,
                "driverId": driver["driverId"],
                "constructorId": constructor["constructorId"],
                "grid_position": int(result["grid"]),
                "finish_position": int(result["position"]),
                "driver_name": f"{driver['givenName']} {driver['familyName']}",
                "constructor_name": constructor["name"]

            })

    return pd.DataFrame(records)


# --------------------------------
# PUBLIC RESULT FUNCTION
# --------------------------------

def get_latest_race_dataframe():

    races = get_last_completed_race()

    return results_to_dataframe(races)


# --------------------------------
# QUALIFYING (SMART FALLBACK)
# --------------------------------

def get_latest_qualifying():

    current_year = get_current_season()

    # try current season qualifying
    data = fetch_json("current/last/qualifying.json")

    races = data["MRData"]["RaceTable"]["Races"]

    if races:
        return races

    # fallback to previous seasons
    for year in range(current_year - 1, 1950, -1):

        data = fetch_json(f"{year}/last/qualifying.json")

        races = data["MRData"]["RaceTable"]["Races"]

        if races:
            return races

    return []


# --------------------------------
# QUALIFYING → DATAFRAME
# --------------------------------

def qualifying_to_dataframe(races):

    records = []

    for race in races:

        race_name = race["raceName"]
        circuit = race["Circuit"]["circuitId"]
        date = race["date"]
        year = int(race["season"])

        for result in race["QualifyingResults"]:

            driver = result["Driver"]
            constructor = result["Constructor"]

            records.append({

                "race_name": race_name,
                "circuitId": circuit,
                "date": date,
                "year": year,
                "driverId": driver["driverId"],
                "constructorId": constructor["constructorId"],
                "grid_position": int(result["position"]),
                "driver_name": f"{driver['givenName']} {driver['familyName']}",
                "constructor_name": constructor["name"]

            })

    return pd.DataFrame(records)


# --------------------------------
# PUBLIC QUALIFYING FUNCTION
# --------------------------------

def get_latest_qualifying_dataframe():

    races = get_latest_qualifying()

    if not races:
        return pd.DataFrame()

    return qualifying_to_dataframe(races)