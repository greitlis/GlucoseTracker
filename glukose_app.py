import streamlit as st
import pandas as pd
from datetime import datetime


def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        
        
def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def eingabe():
    number = st.number_input("Eingabe Blutzuckerwert", value=None, placeholder="Type a number...")
    st.write('Dein aktueller Blutzucker ist ', number)


def main():
    st.title("My Glucose App")
    st.subheader("Enter Data")
    eingabe()


if __name__ == "__main__":
    main()