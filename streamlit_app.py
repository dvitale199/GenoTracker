import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="GenoTracker Data Viewer", layout="wide")

API_URL = "http://127.0.0.1:8000/data"

@st.cache_data
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Failed to fetch data from API")
        return pd.DataFrame()
    
st.title("GenoTracker Data Viewer")
df = fetch_data()

if not df.empty:
    st.write("### Data from GenoTracker API")
    st.dataframe(df)
else:
    st.write("No data available")

if not df.empty:
    st.write("### Data Exploration")
    st.write("#### Summary Statistics")
    st.write(df.describe())

    columns = st.multiselect("Select columns to display", list(df.columns), list(df.columns))
    if columns:
        st.write("#### Selected Columns Data")
        st.dataframe(df[columns])
    else:
        st.write("No columns selected")

    st.write("### Plotting Options")
    plot_type = st.selectbox("Select plot type", ["Line plot", "Bar plot"])
    selected_column = st.selectbox("Select column to plot", list(df.columns))

    if plot_type == "Line plot":
        st.line_chart(df[selected_column])
    elif plot_type == "Bar plot":
        st.bar_chart(df[selected_column])