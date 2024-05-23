import pytz
import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from functions.data import DATA_COLUMNS, DATA_FILE
import functions.data as data
from navigation import logout

st.set_page_config(page_title= "Glukosetracker", page_icon="🩸", layout="centered", initial_sidebar_state="auto", menu_items= None)

def eingabe():
    global blood_sugar
    global measure_date
    global measure_time
    global logged_in_user
    global insulingabe
    
    st.title("Glucosetracker")
    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.image("glucose2_2.jpg")
        col2.image("blooddrop.jpg")
        col3.image("glucose2_2.jpg")
        
    st.subheader("Werteingabe")

    logged_in_user = st.session_state.username
    blood_sugar = st.number_input("Blutzuckerwert in mmol/l", value=None, placeholder="Type a number...", min_value=0.0, max_value=35.0, step=0.1)
    
    # Get the current time in UTC
    utc_now = datetime.now(timezone.utc)

    # Convert UTC time to a European timezone (e.g., Berlin timezone)
    zurich_timezone = pytz.timezone('Europe/Zurich')
    zurich_now = utc_now.replace(tzinfo=pytz.utc).astimezone(zurich_timezone)

    measure_date = st.date_input("Datum", zurich_now, format="DD.MM.YYYY")
    measure_time = st.time_input("Uhrzeit", value = zurich_now.time())
    insulingabe = st.checkbox ("Insulingabe erfolgt")

    st.button("Save", type="primary", on_click=save)

def save():
   
    new_entry = {

        DATA_COLUMNS[0]: logged_in_user,
        DATA_COLUMNS[3]: blood_sugar,
        DATA_COLUMNS[1]: measure_date,
        DATA_COLUMNS[2]: measure_time,
        DATA_COLUMNS[4]: insulingabe
    }
    for key, value in new_entry.items():
        if value == None:
            st.error(f"Bitte ergänze das Feld '{key}'")
            return
        
    new_entry_df = pd.DataFrame([new_entry])

    # Add the new entry to the user's DataFrame
    st.session_state.glucose_data = pd.concat([st.session_state.glucose_data, new_entry_df], ignore_index=True)
    
    # Add the new entry to the DataFrame containing all users' data
    df_all_users = data.get_glucose_df_all_users()
    df_all_users = pd.concat([df_all_users, new_entry_df], ignore_index=True)
    
    # Save the updated DataFrame to GitHub
    commit_msg = f"add measurement at {measure_date} {measure_time}"
    st.session_state.github.write_df(DATA_FILE, df_all_users, commit_msg)

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
    st.button("log out", type="primary", on_click = logout) 
