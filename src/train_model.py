import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from xgboost import XGBClassifier

import joblib

def load_data():
    df = pd.read_csv("data/processed/featured_dataset.csv")
    return df

def prepare_data(df):
    features = ["grid_position", "driver_form", "constructor_form", "driver_consistency", "grid_advantage"]

    df=df.dropna(subset=features + ["is_winner"])
    X=df[features]
    y=df["is_winner"]
    return X,y

def train_model(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\nModel Performance:\n")

    print("Accuracy:", accuracy_score(y_test, y_pred))

    print("ROC-AUC:", roc_auc_score(y_test, y_prob))

    print("\nClassification Report:\n")

    print(classification_report(y_test, y_pred))

    return model


def save_model(model):

    joblib.dump(model, "models/xgboost_f1_model.pkl")

    print("\nModel saved to models/xgboost_f1_model.pkl")


def main():

    print("Loading data...")

    df = load_data()

    print("Preparing features...")

    X, y = prepare_data(df)

    print("Training model...")

    model = train_model(X, y)

    save_model(model)


if __name__ == "__main__":
    main()