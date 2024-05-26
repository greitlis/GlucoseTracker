import streamlit as st
import pandas as pd
from datetime import datetime
import navigation as nav
import functions.user_login as usr 
import functions.data as data

LOGIN_FILE = "credentials.csv"
LOGIN_COLUMNS = ["userName", "pwdHash"]


        
def init_login():
    """Initialize or load the login dataframe."""
    if 'credentials' in st.session_state:
        pass
    elif st.session_state.github.file_exists(LOGIN_FILE):
        st.session_state.credentials = st.session_state.github.read_df(LOGIN_FILE)
    else:
        st.session_state.credentials = pd.DataFrame(columns=LOGIN_COLUMNS)



def init_logged_in():
    if "logged_in" in st.session_state:
        pass
    else:
        st.session_state.logged_in = False


blood_sugar: float
measure_date: datetime.date
measure_time: datetime.time



def main():
    data.init_github()
    init_login()
    init_logged_in()
   #nav.make_sidebar()  
    usr.choice()
    st.image("blooddrop2.jpg")

    if st.session_state.logged_in == True:
        st.switch_page("pages/01_Willkommen.py")
     




if __name__ == "__main__":
    main()