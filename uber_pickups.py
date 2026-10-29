
import streamlit as st
import pandas as pd
import numpy as np

# App title
st.title("Uber Pickups in NYC")

# Dataset settings
DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

# Load and cache the data


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.columns = [str(col).lower() for col in data.columns]
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Display loading status and fetch data
try:
    with st.spinner("Loading Uber pickup data..."):
        data = load_data(10000)

    st.success("Data loaded successfully!")

    # Option to display the raw data
    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.write(data)

    # Histogram of pickups by hour
    st.subheader("Number of pickups by hour")

    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour,
        bins=24,
        range=(0, 24)
    )[0]

    st.bar_chart(hist_values)

    # Interactive hour filter
    hour_to_filter = st.slider(
        "Select an hour",
        min_value=0,
        max_value=23,
        value=17
    )

    filtered_data = data[
        data[DATE_COLUMN].dt.hour == hour_to_filter
    ]

    # Display map
    st.subheader(f"Uber pickups at {hour_to_filter}:00")
    st.map(filtered_data)

    st.caption(
        f"Showing {len(filtered_data):,} pickups "
        f"for the selected hour in the loaded sample."
    )

except Exception as e:
    st.error("The data could not be loaded.")
    st.write("Check your internet connection and try again.")
    st.exception(e)
