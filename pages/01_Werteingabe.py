import streamlit as st
import pandas as pd
from datetime import datetime
from functions.data import DATA_COLUMNS, DATA_FILE
import functions.data as data


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
    

blood_sugar: float
measure_date: datetime.date
measure_time: datetime.time

if __name__ == "__main__":
    if st.session_state.get("logged_in", False)== False:
        st.error("Sie müssen sich zuerst einloggen.")
        st.stop()
        
    data.init_dataframe()
    eingabe()
