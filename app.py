import streamlit as st
from streamlit import session_state as ss
from Modules.nav import menuOptions
import Module_pages.account as account
import Module_pages.homepage as home
import Module_pages.historypage as history
import Module_pages.sortpage as sortPage
import Module_pages.tipspage as tipsPage

st.markdown(
        """
        <h1 style='text-align: center; color: #2E7D32; font-size: 48px;'>♻️ ReSort</h1>
        <h3 style='text-align: center; color: #388E3C;'>Your Smart Waste Sorting Assistant</h3>
        """,
        unsafe_allow_html=True
    )

background_image = """
<style>
[data-testid="stAppViewContainer"] {
background-color: #f4f7e9;
}

[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
}
</style>
"""

st.markdown(background_image, unsafe_allow_html = True)

def set_sidebar_style():
    st.markdown(
        """
        <style>
        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #71936c !important;  /* Soft green tint */
            color: #1b5e20;  /* Dark eco green text */
        }

        </style>
        """,
        unsafe_allow_html=True
    )

style = set_sidebar_style()
selected_page = menuOptions()

if selected_page == "Home":
    home.show()
elif selected_page == "Account":
    account.show()
elif selected_page == "Sort":
    sortPage.show()
elif selected_page == "Tips":
    tipsPage.show()   
elif selected_page == "History":
    history.show()




