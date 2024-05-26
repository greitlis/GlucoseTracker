import streamlit as st
import functions.data as data
from functions.data import DATA_COLUMNS, DATA_FILE
from functions.user_login import LOGIN_COLUMNS
from navigation import logout
import functions.export as export
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages



st.set_page_config(page_title= "Glukosetagebuch", page_icon="📖", layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title("Glukosetagebuch")
with st.container():
        col1, col2, col3 = st.columns(3)
        col1.image("glucose2_2.jpg")
        col2.image("blooddrop_book2.jpg")
        col3.image("glucose2_2.jpg")



def init_tabs():
    tab1, tab2 = st.tabs(["Protokoll :book:", "Verlauf 📈"])
    with tab1:
        df =st.session_state.glucose_data
        VERLAUF_df = st.dataframe(data = df[DATA_COLUMNS], use_container_width=True,
                              column_order= ("measure_date", "measure_time", "blood_sugar", "Insulingabe"),
                              column_config= {
                                "measure_date": st.column_config.Column(label="Datum"),
                                "measure_time": st.column_config.Column(label="Uhrzeit"),
                                "blood_sugar": st.column_config.Column(label="Glukosewert"),
                                "Insulingabe" : st.column_config.CheckboxColumn(
                                "Insulingabe", 
                                default = False,)}, hide_index=True)
    
        # Remove the 'logged_in_user' column
        df = df.drop(columns=['logged_in_user'])

        # Translation dictionary
        translation_dict = {
            'True': 'Ja',
            'False': 'Nein',
            True: 'Ja',
            False: 'Nein'
        }

        # Translate the 'Insulinabgabe' column
        df['Insulingabe'] = df['Insulingabe'].map(translation_dict)

        # Translation dictionary for column titles
        translation_dict_title = {
            'measure_date': 'Messdatum',
            'blood_sugar': 'Blutzucker',
            'measure_time': 'Messzeit'
        }

        # Rename columns using the translation dictionary with title
        df = df.rename(columns=translation_dict_title)


        # Get the binary data of the PDF
        pdf_data = export.dataframe_to_pdf_bytes(df, st.session_state.username)
        username = st.session_state.username
        st.download_button("Download Protokoll", pdf_data, "Messwerte_" + username + ".pdf", help="Downloaden Sie das Protokoll als PDF-Datei", mime="application/pdf")                              
    

    with tab2:
        st.subheader("Verlauf")
        Werte = st.session_state.glucose_data
        Werte['measure_date'] = Werte['measure_date'].astype(str)
        Werte['measure_time'] = Werte['measure_time'].astype(str)
        Werte['Datetime'] = pd.to_datetime(Werte['measure_date'] + ' ' + Werte['measure_time'])
        Werte = Werte.set_index('Datetime')
        tab2.line_chart(data = st.session_state.glucose_data, x = "Datetime", y = ("blood_sugar"), color= None)
        


if __name__ == "__main__":
    if st.session_state.get("logged_in", False)== False:
        st.error("Sie müssen sich zuerst einloggen.")
        st.stop()
    data.init_dataframe_glucose_data()
    init_tabs() 
    st.button("log out", type="primary", on_click = logout)
  
