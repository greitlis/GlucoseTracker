import streamlit as st
import pandas as pd
import hashlib
#from time import sleep

LOGIN_FILE = "credentials.csv"
LOGIN_COLUMNS = ["userName", "pwdHash"]


## Registrierung und login seperate funktionen schreiben und nacheinander schalten, eine aufgabe pro funktion

def choice():
    global userName
    global pwd
    global conf_pwd

    #lf = st.session_state.github.read_df(LOGIN_FILE)
    #st.dataframe(lf)

    choice = st.selectbox("Login / neu registrieren", ["login", "newUser"])
    if choice == "login":
        #login()
        userName = st.text_input("Benutzername")
        pwd = st.text_input("Passwort", type= 'password')

        st.button("login", type="primary", on_click = userLogin)

    else:
        #signup()
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
        st.success("Sie haben sich erfolgreich registriert.")
        #sleep(0.5)
        
        #st.switch_page("pages/GlukoseTraker.py")
        

    else:
        st.text("Das Passwort stimmt nicht mit der Bestätigung überein. \n")
    

#def loginRead():
    #lf = pd.read_csv("...DeinPfad/Auto.csv",sep=";")


def userLogin():

    if userName == "" and pwd == "":
        st.text("Bitte geben Sie einen gültigen Usernamen und ein gültiges Passwort ein. \n")
    elif pwd == "":
        st.text("Bitte geben Sie ein gültiges Passwort ein. \n")
    elif userName == "":
        st.text("Bitte geben Sie einen gültigen Usernamen ein. \n")
    else:
        lf = st.session_state.github.read_df(LOGIN_FILE)
        
        user_list = lf["userName"]

        for item in user_list:
            if item == userName:
                pwd_check()

def pwd_check():
    lf = st.session_state.github.read_df(LOGIN_FILE)
    auth = pwd.encode()
    valHash = hashlib.sha3_512(auth).hexdigest() 
    pwd_list = lf["pwdHash"]

    for item in pwd_list:
        if item == valHash:
            st.session_state.logged_in = True
            st.text(f"login erfolgreich, Willkommen {userName}")
            #sleep(0.5)
            #st. switch_page("pages/GlukoseTraker.py")
            

       

