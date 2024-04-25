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
    global blood_sugar
    global measure_date
    global measure_time

    blood_sugar = st.number_input("Eingabe Blutzuckerwert", value=None, placeholder="Type a number...", min_value=0, max_value=35)
    st.write('Dein aktueller Blutzucker ist ', blood_sugar)

    measure_date = st.date_input("Eingabe Datum", datetime.now(), format="DD.MM.YYYY")
    measure_time = st.time_input("Eingabe Uhrzeit", datetime.now())

    st.write('Datum/Uhrzeit: ' + str(measure_date) + ' ' + str(measure_time))

    st.button("Save", type="primary", on_click=save)

def save():
    st.write('I would now save!')
    st.write('Wert', blood_sugar)
    st.write('Datum/Uhrzeit:', measure_date, measure_time)

    # TODO: Save to CSV

blood_sugar: float
measure_date: datetime.date
measure_time: datetime.time


def main():
    st.title("My Glucose App")
    st.subheader("Enter Data")
    eingabe()


if __name__ == "__main__":
    main()