import joblib
import pandas as pd
import os


# Resolve model path relative to the project root, regardless of CWD
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "xgboost_f1_model.pkl")


def load_model():

    model = joblib.load(MODEL_PATH)

    return model


def predict_win_probability(features_dict):

    model = load_model()

    feature_order = [
        "grid_position",
        "driver_form",
        "constructor_form",
        "driver_consistency",
        "grid_advantage"
    ]

    input_df = pd.DataFrame([features_dict])

    input_df = input_df[feature_order]

    prob = model.predict_proba(input_df)[0][1]

    return prob


if __name__ == "__main__":

    sample_driver = {
        "grid_position": 1,
        "driver_form": 2.1,
        "constructor_form": 2.3,
        "driver_consistency": 1.2,
        "grid_advantage": 1.1
    }

    prob = predict_win_probability(sample_driver)

    print(f"Win Probability: {prob:.2%}")