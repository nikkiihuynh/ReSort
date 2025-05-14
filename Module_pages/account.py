import streamlit as st
from streamlit import session_state as ss
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
from Modules.database import connect_to_db, fetch_users_from_db, insert_user, user_exists
import yaml
from yaml.loader import SafeLoader

CONFIG_FILENAME = 'config.yaml'

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


def show():
    credentials = fetch_users_from_db()

    authenticator = stauth.Authenticate(
        credentials,
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    if "logout" not in st.session_state:
        st.session_state["logout"] = False

    for key in ["name", "authentication_status", "username"]:
        if key not in st.session_state:
            st.session_state[key] = None

    login_tab, register_tab = st.tabs(['Login', 'Register'])

    with login_tab:
        fields = {"Form name": "Login", "Username": "Email", "Password": "Password", "Login": "Login"}
        name, authentication_status, username = authenticator.login(fields=fields, location="main")

        if authentication_status:
            ss["username"] = username
            authenticator.logout("Logout", "sidebar")
            st.success(f"Welcome {ss['name']}") 
        elif ss["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif ss["authentication_status"] is None:
            st.warning('Please enter your username and password')

    with register_tab:
        if authentication_status:
            st.warning(f"Must log-out to register another account")            
        else:
            with st.form("register"):
                st.markdown("#### Register")
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Register")

                if submit:
                    if email and password and username:
                        if user_exists(email):
                            st.error("Email already registered. Please log in.")
                        else:
                            hashed_pw = Hasher([password]).generate()[0]
                            insert_user(username, email, hashed_pw)
                            st.success("Registration successful! You can now log in.")
                            st.rerun() 
                    else:
                        st.error("Please fill in all fields.")

