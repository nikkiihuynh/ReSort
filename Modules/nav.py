import streamlit as st
from streamlit_option_menu import option_menu
from streamlit import session_state as ss

def menuOptions():
    menu_options = ["Home", "Account"]
    menu_icons = ["house", "lock"]

    if 'authentication_status' not in ss:
        ss.authentication_status = False

    if ss["authentication_status"]:
        menu_options += ["Sort", "History"]
        menu_icons += ["recycle", "book"]

    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=menu_options,
            icons=menu_icons,
            menu_icon="list",
            default_index=0
        )


    return selected