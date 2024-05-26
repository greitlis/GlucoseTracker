import streamlit as st
import pandas as pd
from functions.github_contents import GithubContents

DATA_FILE = "glucose_measurements.csv"
DATA_COLUMNS = ["logged_in_user", "measure_date", "measure_time","blood_sugar", "Insulingabe"]

VERORD_FILE = "Verordnungen.csv"
VERORD_COLUMNS = ["logged_in_user", "arzt", "telefon", "basis", "gabe_basis", "frequenz", "wann", "kurz", "gabe_kurz", "frequenz_kurz", "wann_kurz"]


def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        

def init_dataframe_glucose_data():
    """Initialize or load the dataframe glucose data."""
    if 'glucose_data' in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        df = st.session_state.github.read_df(DATA_FILE)
        df_filter = df.loc[df[DATA_COLUMNS[0]]== st.session_state.username] 
        st.session_state.glucose_data = df_filter
    else:
        st.session_state.glucose_data = pd.DataFrame(columns=DATA_COLUMNS)

def init_dataframe_verordnungen():
    """Initialize or load the dataframe verordnungen."""
    if 'verordnungen' in st.session_state:
        pass
    elif st.session_state.github.file_exists(VERORD_FILE):
        df = st.session_state.github.read_df(VERORD_FILE)
        df_filter = df.loc[df[VERORD_COLUMNS[0]]== st.session_state.username] 
        st.session_state.verordnungen = df_filter
    else:
        st.session_state.verordnungen = pd.DataFrame(columns=VERORD_COLUMNS)

def get_glucose_df_all_users():
    if st.session_state.github.file_exists(DATA_FILE):
        df = st.session_state.github.read_df(DATA_FILE)
    else:
        df = pd.DataFrame(columns=DATA_COLUMNS)
    return df

def get_verordnungen_df_all_users():
    if st.session_state.github.file_exists(VERORD_FILE):
        df = st.session_state.github.read_df(VERORD_FILE)
    else:
        df = pd.DataFrame(columns=VERORD_COLUMNS)
    return df

def update_row_with_dict(df,d,idx):
    df.loc[idx,d.keys()] = d.values()
