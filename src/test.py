import requests

url = "https://api.jolpi.ca/ergast/f1/2025/last/results.json"

data = requests.get(url).json()

races = data["MRData"]["RaceTable"]["Races"]

print(len(races))
print(races[0]["raceName"])