import streamlit as st
from streamlit_option_menu import option_menu
from streamlit import session_state as ss

def menuOptions():
    menu_options = ["Home", "Account"]
    menu_icons = ["house", "lock"]

    if 'authentication_status' not in ss:
        ss.authentication_status = False

    if ss["authentication_status"]:
        menu_options += ["Sort", "Tips", "History"]
        menu_icons += ["recycle", "lightbulb", "book"]

    with st.sidebar:
        selected = option_menu(
            menu_title="♻️ ReSort",
            options=menu_options,
            icons=menu_icons,
            menu_icon="list",
            default_index=0,
            styles={
                "container": {
                    "padding": "10px",
                    "background-color": "#e6f4ea",  
                    "border-radius": "8px"
                },
                "icon": {
                    "color": "#2e7d32",  
                    "font-size": "18px"
                },
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "--hover-color": "#c8e6c9",  
                    "color": "#1b5e20", 
                    "border-radius": "5px"
                },
                "nav-link-selected": {
                    "background-color": "#81c784",  
                    "color": "white",
                    "font-weight": "bold"
                },
            }
        )

    return selected
