import pandas as pd

def add_driver_form(df, window=5):
    df=df.sort_values(by=["driverId","date"])
    df["driver_form"]=df.groupby("driverId")["finish_position"].rolling(window, min_periods=1).mean().shift(1).reset_index(0,drop=True)
    return df

def main():
    df=pd.read_csv("../data/processed/eda_dataset.csv")

    df=add_driver_form(df)

    df.to_csv("../data/processed/featured_dataset.csv", index=False)

    print("Feature Engineering completed and saved to ../data/processed/featured_dataset.csv")

    print(df[["driver_name","date","finish_position","driver_form"]].head(15))

if __name__ == "__main__":
    main()