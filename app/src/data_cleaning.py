import pandas as pd
from data_loader import load_data

def create_master_dataset():
    data = load_data()

    races=data["races"]
    results=data["results"]
    drivers=data["drivers"]
    constructors=data["constructors"]
    qualifying=data["qualifying"]

    #Merge results + races

    df=results.merge(races[["raceId","year","name","date","circuitId"]], on="raceId", how="left")

    #Merge drivers
    df=df.merge(drivers[["driverId","forename","surname","nationality"]], on="driverId", how="left")

    #Merge constructors
    df=df.merge(constructors[["constructorId","name","nationality"]], on="constructorId", how="left", suffixes=("", "_constructor"))

    #Merge qualifying
    df=df.merge(qualifying[["raceId","driverId","position"]], on=["raceId","driverId"], how="left", suffixes=("", "_quali"))

    # Rename columns for clarity
    df.rename(columns={
        "position": "finish_position",
        "position_quali": "grid_position",
        "name": "race_name",
        "name_constructor": "constructor_name"}, inplace=True)
    
    #Create driver full name
    df["driver_name"]=df["forename"]+" "+df["surname"]

    return df

if __name__ == "__main__":

    df=create_master_dataset()

    print(df.shape)
    print(df.head())

    df.to_csv("../data/processed/master_dataset.csv", index=False)

    print("Master dataset created and saved to ../data/processed/master_dataset.csv")