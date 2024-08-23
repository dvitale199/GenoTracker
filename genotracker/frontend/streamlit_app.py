import streamlit as st
import pandas as pd
import requests
from google.cloud import secretmanager
from datetime import datetime

st.set_page_config(page_title="GenoTracker Data Viewer", layout="wide")

API_URL = "https://genotracker-fastapi-3wsqie35cq-uc.a.run.app/data"
#debug
# API_URL = "http://0.0.0.0:8080/data"

def access_secret_version():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/776926281950/secrets/genotracker-api-key/versions/1"
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode("UTF-8")

API_KEY = access_secret_version()

def get_last_modified_time():
    headers = {"X-API-Key": API_KEY}
    response = requests.head(API_URL, headers=headers)
    if response.status_code == 200:
        last_modified_str = response.headers.get("Last-Modified")
        if last_modified_str:
            return datetime.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S GMT")
    return datetime.now()

@st.cache_data(show_spinner=False)
def fetch_data(from_gcs: bool = True, last_modified: datetime = None):
    params = {"from_gcs": from_gcs}
    headers = {"X-API-Key": API_KEY}
    try:
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        #debug
        # st.write("Raw API Data:", data)
        
        if isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], dict):
                df = pd.DataFrame(data)
            else:
                st.error(f"Unexpected data format: list contains non-dict items or is empty.")
                df = pd.DataFrame()
        else:
            st.error(f"Unexpected data type received from the API: {type(data)}")
            df = pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from API: {e}")
        df = pd.DataFrame()
    except ValueError as e:
        st.error(f"Error converting data to DataFrame: {e}")
        df = pd.DataFrame()
    
    return df

st.title("GenoTracker Data Viewer")

# Get the last modified time to use as a cache buster
last_modified = get_last_modified_time()
df = fetch_data(last_modified=last_modified)

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