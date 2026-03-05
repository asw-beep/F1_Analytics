import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from xgboost import XGBClassifier
import joblib


FEATURES = [
    "grid_position",
    "driver_form",
    "constructor_form",
    "driver_consistency",
    "grid_advantage",
    "driver_circuit_avg_finish",
    "constructor_season_avg_finish"
]


def load_data():
    df = pd.read_csv("data/processed/featured_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def prepare_data(df):
    df = df.dropna(subset=FEATURES + ["is_winner"])
    return df


def time_based_split(df):

    train_df = df[df["year"] <= 2021]
    test_df = df[df["year"] > 2021]

    X_train = train_df[FEATURES]
    y_train = train_df["is_winner"]

    X_test = test_df[FEATURES]
    y_test = test_df["is_winner"]

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):

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

    return model


def evaluate_model(model, X_test, y_test):

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\nModel Performance (Time-Based Split):\n")

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))

    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))


def save_model(model):
    joblib.dump(model, "models/xgboost_f1_model.pkl")
    print("\nModel saved to models/xgboost_f1_model.pkl")


def main():

    print("Loading data...")
    df = load_data()

    print("Preparing data...")
    df = prepare_data(df)

    print("Splitting data (1950–2021 train, 2022–2024 test)...")
    X_train, X_test, y_train, y_test = time_based_split(df)

    print("Training model...")
    model = train_model(X_train, y_train)

    print("Evaluating model...")
    evaluate_model(model, X_test, y_test)

    save_model(model)


if __name__ == "__main__":
    main()