import requests
import pandas as pd


def get_latest_completed_race():

    url = "https://api.jolpi.ca/ergast/f1/2025/last/results.json"

    data = requests.get(url).json()

    races = data["MRData"]["RaceTable"]["Races"]

    records = []

    for race in races:

        race_name = race["raceName"]
        circuit = race["Circuit"]["circuitId"]
        date = race["date"]
        year = int(race["season"])

        for result in race["Results"]:

            records.append({
                "race_name": race_name,
                "circuitId": circuit,
                "date": date,
                "year": year,
                "driverId": result["Driver"]["driverId"],
                "constructorId": result["Constructor"]["constructorId"],
                "grid_position": int(result["grid"]),
                "finish_position": int(result["position"])
            })

    return pd.DataFrame(records)