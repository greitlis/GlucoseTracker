import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():
    with st.sidebar:
        
        if st.session_state.get("logged_in", False):
            st.page_link("pages/01_Werteingabe.py", label="Werteingabe", icon="💉")

            if st.button("Log out"):
                    logout()
        elif get_current_page_name() != "glukose_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("glukose_app.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("glukose_app.py")