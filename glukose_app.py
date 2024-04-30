import streamlit as st
import pandas as pd
from datetime import datetime
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


def eingabe():
    global blood_sugar
    global measure_date
    global measure_time

    st.title("Glucosetracker")
    st.subheader("Werteingabe")

    blood_sugar = st.number_input("Blutzuckerwert in mmol/l", value=None, placeholder="Type a number...", min_value=0.0, max_value=35.0, step=0.1)

    measure_date = st.date_input("Datum", datetime.now(), format="DD.MM.YYYY")
    measure_time = st.time_input("Uhrzeit", datetime.now())

    st.button("Save", type="primary", on_click=save)

def save():
    new_entry = {
        DATA_COLUMNS[0]: blood_sugar,
        DATA_COLUMNS[1]: measure_date,
        DATA_COLUMNS[2]: measure_time
    }
    for key, value in new_entry.items():
        if value == None:
            st.error(f"Bitte ergänze das Feld '{key}'")
            return
        
    new_entry_df = pd.DataFrame([new_entry])
    st.session_state.glucose_data = pd.concat([st.session_state.glucose_data, new_entry_df], ignore_index=True)

    # Save the updated DataFrame to GitHub
    commit_msg = f"add measurement at {measure_date} {measure_time}"
    st.session_state.github.write_df(DATA_FILE, st.session_state.glucose_data, commit_msg)

    st.success("Der Glukose-Wert wurde erfolgreich gespeichert!")

def uebersicht():
    st.title("Glucosetracker")
    st.subheader("Übersicht der gespeicherten Werte")
    st.dataframe(st.session_state.glucose_data)

blood_sugar: float
measure_date: datetime.date
measure_time: datetime.time


def main():
    init_github()
    init_dataframe()
    with st.sidebar.container():
        st.sidebar.title("Glucosetracker 💉")
        seiten= {
            "Werteingabe": eingabe,
            "Übersicht": uebersicht
        }
        auswahl = st.sidebar.radio("", list(seiten.keys()))

    seiten[auswahl]()


if __name__ == "__main__":
    main()