import streamlit as st
from streamlit import session_state as ss
from Modules.nav import menuOptions
import Module_pages.account as account
import Module_pages.homepage as home
import Module_pages.historypage as history
import Module_pages.sortpage as sortPage

selected_page = menuOptions()

st.title("ReSort")

if selected_page == "Home":
    home.show()
elif selected_page == "Account":
    account.show()
elif selected_page == "Sort":
    sortPage.show()
elif selected_page == "History":
    history.show()