## Festlegen des Insulinschemas, je nach user verschieden, daher noch nicht festgelegt.
import streamlit as st
from time import sleep
from navigation import logout
st.set_page_config(page_title= "Verordnungen", page_icon="📋", layout="centered", initial_sidebar_state="auto", menu_items=None)

def prescriptions():
    st.title("Glucosetracker")
    st.subheader("Verordnungen 📋")
    st.write("Hier können Sie Ihr Insulinschema festlegen.")
    st.write("Bitte beachten Sie, dass dies nur eine Empfehlung ist und keine ärztliche Beratung ersetzt.")
    st.write("Bitte wenden Sie sich an Ihren Arzt, um Ihr Insulinschema festzulegen.")

if __name__ == "__main__":
    if st.session_state.get("logged_in", False)== False:
        st.error("Sie müssen sich zuerst einloggen.")
        st.stop()
    prescriptions()
st.button("log out", type="primary", on_click = logout)
