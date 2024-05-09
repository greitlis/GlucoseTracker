import streamlit as st
import pandas as pd
from functions.github_contents import GithubContents

DATA_FILE = "glucose_measurements.csv"
DATA_COLUMNS = ["blood_sugar", "measure_date", "measure_time"]

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'glucose_data' in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.glucose_data = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.glucose_data = pd.DataFrame(columns=DATA_COLUMNS)