import streamlit as st
from functions.user_login import LOGIN_COLUMNS
from navigation import logout
from time import sleep
import functions.data as data



st.set_page_config(page_title= "Willkommen", page_icon= None, layout="wide", initial_sidebar_state="auto", menu_items= None)


def set_welcome_page():
    username = st.session_state.username
    with st.container(border = True):
        col1, col2 = st.columns(2, gap = "large")
        col1.title(f"Willkommen {username}")
        col2.image("pictures/blooddrop_hello.jpg")


    st.subheader("GlukoseTracker for KIDS")
    st.image("pictures/blooddrop_what.jpg")
    st.write("Wie die APP funktioniert:")

    with st.container():
        row1= st.write("🩸 Werteingabe: Gib hier deinen gemessenen Blutzuckerwert ein und bestätige mit einem Häkchen, ob du Insulin gespritzt hast.")
        row2 = st.write("📖 Glukosetagebuch: Auf dieser Seite werden deine eingetragenen Werte in einer Tabelle dargestellt. Du kannst sie dir auch im Verlauf als Kurve anschauen.")
        row3 = st.write("📋 Verordnungen: Hier findest du die Telefonnummer deiner Ärztin/deines Arztes, die Insulinverordnungen und weiter unten ein Schema wann du welches Insulin spritzen musst.")


if __name__ == "__main__":
    if st.session_state.get("logged_in", False)== False:
        st.error("Sie müssen sich zuerst einloggen.")
        st.stop()
    data.init_dataframe_glucose_data()
    set_welcome_page()
    st.button("Log out", type="primary", on_click = logout)

