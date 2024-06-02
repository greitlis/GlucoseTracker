import streamlit as st
import pandas as pd
import hashlib


LOGIN_FILE = "credentials.csv"
LOGIN_COLUMNS = ["userName", "pwdHash"]



def choice():
    global userName
    global pwd
    global conf_pwd

    choice_login = "Login"  

    choice = st.selectbox("Login / neu registrieren", [choice_login, "Registrieren"])
    if choice == choice_login:

        userName = st.text_input("Benutzername")
        pwd = st.text_input("Passwort", type= 'password')

        st.button("Login", type="primary", on_click = userLogin)

    else:
        
        userName = st.text_input("Benutzername")
        pwd = st.text_input("Passwort", type = 'password')
        conf_pwd = st.text_input("Passwort bestätigen", type = 'password')

        if st.button("registrieren", type = "primary"):
            registerUser()


def registerUser():

    if userName == "" and pwd == "":
        st.text("Bitte geben Sie einen gültigen Usernamen und ein gültiges Passwort ein. \n")
    elif conf_pwd == "":
        st.text("Bitte bestätigen Sie Ihr Passwort. \n")
    elif pwd == "":
        st.text("Bitte geben Sie ein gültiges Passwort ein. \n")
    elif userName == "":
        st.text("Bitte geben Sie einen gültigen Usernamen ein. \n")
    elif pwd == conf_pwd:
            
        # Check if the username already exists
        if userName in st.session_state.credentials[LOGIN_COLUMNS[0]].values:
            st.error("Benutzername existiert bereits. Bitte wählen Sie einen anderen.")
            return

        encoded_pwd = conf_pwd.encode()
        pwdHash = hashlib.sha3_512(encoded_pwd).hexdigest()

        new_entry = {
            LOGIN_COLUMNS[0]: userName,
            LOGIN_COLUMNS[1]: pwdHash
        }
        for key, value in new_entry.items():
            if value == None:
                st.error(f"Bitte ergänze das Feld '{key}'")
                return
            
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.credentials = pd.concat([st.session_state.credentials, new_entry_df], ignore_index=True)

        # Save the updated DataFrame to GitHub
        commit_msg = f"add user {userName}"
        st.session_state.github.write_df(LOGIN_FILE, st.session_state.credentials, commit_msg)
        st.session_state.logged_in = True
        st.session_state.username = userName
        st.success("Sie haben sich erfolgreich registriert.")
            

    else:
        st.text("Das Passwort stimmt nicht mit der Bestätigung überein. \n")
    




def userLogin():

    if userName == "" and pwd == "":
        st.text("Bitte geben Sie einen gültigen Usernamen und ein gültiges Passwort ein. \n")
    elif pwd == "":
        st.text("Bitte geben Sie ein gültiges Passwort ein. \n")
    elif userName == "":
        st.text("Bitte geben Sie einen gültigen Usernamen ein. \n")
    else:
        lf = st.session_state.github.read_df(LOGIN_FILE)
        
        userfound = False 
        for index,row in lf.iterrows():
            if row[LOGIN_COLUMNS[0]] == userName:
                userfound = True
                is_pwd_right = pwd_check(row[LOGIN_COLUMNS[1]])
                if is_pwd_right == True:
                    st.session_state.logged_in = True
                    st.session_state.username = userName
                    st.text(f"login erfolgreich, Willkommen {userName}")
                else:
                    st.error("Falsches Passwort oder Benutzername")
                break 
        if userfound == False:
            st.error("Falsches Passwort oder Benutzername")
            

def pwd_check(pwdHash):
    auth = pwd.encode()
    valHash = hashlib.sha3_512(auth).hexdigest() 
    if valHash == pwdHash:
        return True    
    else:
        return False
        