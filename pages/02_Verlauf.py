## Funktionen zum visualisieren der eingertegenen Werte über eine bestimmten Zeitraum
import streamlit as st
import functions.data as data

st.set_page_config(page_title= "Verlauf", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

def uebersicht():
    st.title("Glucosetracker")
    st.subheader("Übersicht der gespeicherten Werte")
    st.dataframe(st.session_state.glucose_data)

if __name__ == "__main__":
    if st.session_state.get("logged_in", False)== False:
        st.error("Sie müssen sich zuerst einloggen.")
        st.stop()
    data.init_dataframe()
    uebersicht()