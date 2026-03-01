import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("../src"))

from predict import predict_win_probability
from feature_lookup import get_latest_driver_features, get_all_drivers


st.title("F1 Race Winner Prediction System")


drivers = get_all_drivers()

selected_driver = st.selectbox("Select Driver", drivers)


if st.button("Predict Win Probability"):

    features = get_latest_driver_features(selected_driver)

    prob = predict_win_probability(features)

    st.success(f"{selected_driver} Win Probability: {prob:.2%}")

    st.write("Driver Features Used:")
    st.json(features)


def get_latest_driver_features(driver_name):
    # This function should return the latest features for the given driver
    # For example, you might return a dictionary with the driver's name,
    # age, and other relevant features
    return {"name": driver_name, "age": 30}