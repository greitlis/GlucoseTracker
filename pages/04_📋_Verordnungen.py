## Festlegen des Insulinschemas, je nach user verschieden, daher noch nicht festgelegt.
import streamlit as st
import pandas as pd
from navigation import logout
import functions.data as data
st.set_page_config(page_title= "Verordnungen", page_icon="📋", layout="wide", initial_sidebar_state="auto", menu_items=None)



with st.container():
    col1, col2 = st.columns(2, gap = "small")
    col1.title("Verordnungen")
    col2.image("pictures/protokoll.jpg")


def eingabe_verordnungen():
    global arzt
    global telefon
    global basis
    global gabe_basis
    global frequenz
    global wann
    global kurz
    global gabe_kurz
    global frequenz_kurz
    global wann_kurz

    # Get the user's data from the DataFrame
    df = st.session_state.verordnungen.fillna('')

    arzt = "" if df.empty else df[data.VERORD_COLUMNS[1]].values[0]
    telefon = "" if df.empty else df[data.VERORD_COLUMNS[2]].values[0]
    basis = "" if df.empty else df[data.VERORD_COLUMNS[3]].values[0]
    gabe_basis = "" if df.empty else df[data.VERORD_COLUMNS[4]].values[0]
    frequenz = "" if df.empty else df[data.VERORD_COLUMNS[5]].values[0]
    wann = "" if df.empty else df[data.VERORD_COLUMNS[6]].values[0]
    kurz = "" if df.empty else df[data.VERORD_COLUMNS[7]].values[0]
    gabe_kurz = "" if df.empty else df[data.VERORD_COLUMNS[8]].values[0]
    frequenz_kurz = "" if df.empty else df[data.VERORD_COLUMNS[9]].values[0]
    wann_kurz = "" if df.empty else df[data.VERORD_COLUMNS[10]].values[0]

    if "disabled" not in st.session_state:
            st.session_state["disabled"] = True

    def enable():
        st.session_state["disabled"] = False

           

## Angaben Ärztin/Arzt:
    st.subheader("Angaben Ärztin/Arzt")
    arzt = st.text_input(label = "Deine Ärztin/ dein Arzt:", disabled = st.session_state.disabled, value = arzt)
    telefon = st.text_input(label =" ☎ Telefonnummer:", disabled = st.session_state.disabled, value = telefon)

## Insulingabe:
    st.subheader("Insulin")

    with st.container():
        verabreichungsformen = ["in Oberschenkel", "in Bauchfalte"]
        row1 = col1, col2, col3, col4 = st.columns(4)

        basisinsulin_werte = ["Insulatard", "Lantus", "Levemir", "Tresiba"]
        basis_index = basisinsulin_werte.index(basis) if basis in basisinsulin_werte else 0
        basis = col1.selectbox("🐌 Basisinsulin", basisinsulin_werte,disabled = st.session_state.disabled, index = basis_index)
        gabe_basis_index = verabreichungsformen.index(gabe_basis) if gabe_basis in verabreichungsformen else 0
        gabe_basis = col2.selectbox("Verabreichungsform", verabreichungsformen, key="gabe_basis", disabled=st.session_state.disabled, index = gabe_basis_index)
        frequenz = col3.text_input("Wie oft?", disabled = st.session_state.disabled, value = frequenz)
        wann = col4.text_input("Wann?", disabled = st.session_state.disabled, value = wann)
        row2 = col1, col2, col3, col4 = st.columns(4)
        kurzinsulin_werte = ["Actrapid", "Novorapid"]
        kurz_index = kurzinsulin_werte.index(kurz) if kurz in kurzinsulin_werte else 0
        kurz = col1.selectbox("🚀 Kurz wirksames Insulin", kurzinsulin_werte, disabled = st.session_state.disabled, index = kurz_index)
        gabe_kurz_index = verabreichungsformen.index(gabe_kurz) if gabe_kurz in verabreichungsformen else 0
        gabe_kurz = col2.selectbox("Verabreichungsform", verabreichungsformen, key="gabe_kurz", disabled=st.session_state.disabled, index = gabe_kurz_index)
        frequenz_kurz = col3.text_input(" ", disabled = st.session_state.disabled, value = frequenz_kurz)
        wann_kurz = col4.text_input("", disabled = st.session_state.disabled, value= wann_kurz)
    
    st.button("Bearbeiten", on_click = enable, disabled= not st.session_state.disabled)
    st.button("Änderungen speichern", on_click = save_eingabe_verordnungen, disabled= st.session_state.disabled)




def save_eingabe_verordnungen():

    username = st.session_state.username

    entry_verordnungen = {
        data.VERORD_COLUMNS[0] : username,
        data.VERORD_COLUMNS[1] : arzt,
        data.VERORD_COLUMNS[2] : telefon,
        data.VERORD_COLUMNS[3] : basis,
        data.VERORD_COLUMNS[4] : gabe_basis,
        data.VERORD_COLUMNS[5] : frequenz,
        data.VERORD_COLUMNS[6] : wann,
        data.VERORD_COLUMNS[7] : kurz,
        data.VERORD_COLUMNS[8] : gabe_kurz,
        data.VERORD_COLUMNS[9] : frequenz_kurz,
        data.VERORD_COLUMNS[10] : wann_kurz
    }

    entry_verordnungen_df = pd.DataFrame([entry_verordnungen])

    # Set the new entry as the user's dataframe (only 1 per user)
    st.session_state.verordnungen = entry_verordnungen_df
 
    # Get all verordnungen to save it to GitHub
    df_all_users = data.get_verordnungen_df_all_users()

    # Check if the user already exists in the DataFrame
    index = df_all_users.loc[df_all_users[data.VERORD_COLUMNS[0]] == username].index 

    # If the user does not exist in the DataFrame, add the new entry
    if index.empty:
        df_all_users = pd.concat([df_all_users, entry_verordnungen_df], ignore_index=True)
    else:
        # If the user already exists in the DataFrame, update the entry
        data.update_row_with_dict(df_all_users, entry_verordnungen, index[0])
    
    # Save the updated DataFrame to GitHub
    commit_msg = f"add verordnung for {username}" 
    st.session_state.github.write_df(data.VERORD_FILE, df_all_users, commit_msg)

    st.success("Die Änderungen wurden erfolgreich gespeichert")
    
    st.session_state["disabled"] = True # Text input widgets sollen nach speichern wieder nicht editierbar sein.
    





if __name__ == "__main__":
    if st.session_state.get("logged_in", False)== False:
        st.error("Sie müssen sich zuerst einloggen.")
        st.stop()
   
    data.init_dataframe_verordnungen()
    eingabe_verordnungen()
    
    

    st.button("log out", type="primary", on_click = logout)
