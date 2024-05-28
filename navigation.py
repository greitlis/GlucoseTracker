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
            st.page_link("pages/Home.py", label="Home", icon= None)

            
        elif get_current_page_name() != "Home":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("Home.py")


def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    del st.session_state["glucose_data"]
    del.st.session_state["verordnungen"]
    st.info("Sie haben sich erfolgreich ausgeloggt")