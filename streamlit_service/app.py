import streamlit as st
import pandas as pd
import requests
import urllib3

# urllib3.disable_warnings(category = urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="GenoTracker Data Viewer", layout="wide")

API_URL = "https://genotracker-dot-gp2-release-terra.uc.r.appspot.com/data"

@st.cache_data
def fetch_data():
    # response = requests.get(API_URL, verify=False)
    response = requests.get(API_URL)
    if response.status_code == 200:
        print(response)
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

bar_plot_columns = [
    'n_dna_samples_attempted', 'total_qc_pass',
    'callrate_fails', 'sex_fails', 'het_fails', 'duplicates', 'afr_case', 'afr_control',
    'afr_other', 'aac_case', 'aac_control', 'aac_other', 'aj_case',
    'aj_control', 'aj_other', 'eas_case', 'eas_control', 'eas_other',
    'eur_case', 'eur_control', 'eur_other', 'fin_case', 'fin_control',
    'fin_other', 'amr_case', 'amr_control', 'amr_other', 'sas_case',
    'sas_control', 'sas_other', 'cas_case', 'cas_control', 'cas_other',
    'mde_case', 'mde_control', 'mde_other', 'cah_case', 'cah_control',
    'cah_other', 'total'
]

if not df.empty:
    st.write("### Data Exploration")

    selected_column = st.selectbox("Select column to plot", bar_plot_columns)

    selected_studies = st.multiselect("Select study codes to include (leave empty to include all)", df['study_code'].unique())

    if selected_studies:
        filtered_df = df[df['study_code'].isin(selected_studies)]
    else:
        filtered_df = df

    grouped_df = filtered_df.groupby('study_code')[selected_column].sum().reset_index()
    sorted_df = grouped_df.sort_values(by=selected_column, ascending=False)

    def create_bar_plot(column_name, data):
        st.write(f"### Bar Plot for {column_name} by Study Code")
        st.bar_chart(data.set_index('study_code'))

    create_bar_plot(selected_column, sorted_df)

if __name__ == "__main__":
    fetch_data()