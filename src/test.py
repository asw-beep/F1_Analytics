from api_handler import get_latest_race_dataframe

df = get_latest_race_dataframe()

print(df.head())
print(df.shape)