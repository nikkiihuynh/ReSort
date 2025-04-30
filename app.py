import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import sort
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import plotly.express as px
<<<<<<< Updated upstream
=======
import pandas as pd
from PIL import Image
>>>>>>> Stashed changes

# --- Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.title {
    position: relative;
    top: -70px;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<h1 class="title">ReSort</h1>', unsafe_allow_html=True)

# --- Database Connection ---
def connectToDB():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='password',
        database='resort'
    )

# --- Fetch Users from DB ---
def fetch_users_from_db():
    conn = connectToDB()
    cursor = conn.cursor()
    cursor.execute("SELECT name, password, email FROM USER")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    names, passwords, emails = [], [], []
    for name, password, email in users:
        emails.append(email)
        names.append(name)
        passwords.append(password)
    return emails, names, passwords

emails, names, hashed_passwords = fetch_users_from_db()

for key in ["authentication_status", "username", "name", "selected"]:
    if key not in st.session_state:
        st.session_state[key] = None

credentials = {
    'usernames': {
        email: {
            'name': name,
            'password': hashed_pw,
            'email': email,
            'roles': []  
        } for email, name, hashed_pw in zip(emails, names, hashed_passwords)
    }
}

# --- Authentication Setup ---
authenticator = stauth.Authenticate(
    credentials,
    "resort_app",  # cookie_name
    "abcdef",      # key
    cookie_expiry_days=30,
)

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None
if "selected" not in st.session_state:
    st.session_state["selected"] = None
    
# --- Login ---
fields = {"Form name": "Login", "Username": "Email", "Password": "Password", "Login": "Login"}

if st.session_state.get("authentication_status") is None:
    name, authentication_status, username = authenticator.login(fields=fields, location="main")
    st.session_state["authentication_status"] = authentication_status
    st.session_state["username"] = username
    st.session_state["name"] = name
else:
    authentication_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")
    name = st.session_state.get("name")

# --- Save login info ---
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None

authentication_status = st.session_state.get("authentication_status")
email = st.session_state.get("username")
name = st.session_state.get("name")

# --- Sidebar ---
with st.sidebar:
    # Initialize menu_options and menu_icons with default values
    menu_options = ["Register"]
    menu_icons = ["key"]
    
    # Update based on authentication status
    if st.session_state.get("authentication_status") is True:
        menu_options = ["Home", "Sort", "History"]
        menu_icons = ["house", "recycle", "book"]
    elif st.session_state.get("authentication_status") is False:
        menu_options = ["Register"]
        menu_icons = ["key"]
    
    # Ensure we always have valid options
    if not menu_options:
        menu_options = ["Register"]
        menu_icons = ["key"]

    # Set default index
    default_index = 0
    if st.session_state.selected in menu_options:
        default_index = menu_options.index(st.session_state.selected)

    selected = option_menu(
        menu_title="Main Menu",
        options=menu_options,
        icons=menu_icons,
        menu_icon="list",
        default_index=default_index,
        key="main_menu"
    )
    st.session_state.selected = selected

    if st.session_state.get("authentication_status"):
        authenticator.logout("Logout", "sidebar")

# Register logic 
if not authentication_status and st.session_state.get("selected") == "Register":
    with st.form("register"):
        st.markdown("#### Register")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            if email and password and username:
                conn = connectToDB()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM USER WHERE email = %s", (email,))
                if cursor.fetchone():
                    st.error("Email already registered. Please log in.")
                else:
                    hashed_pw = Hasher([password]).generate()[0]
                    cursor.execute("INSERT INTO USER (name, email, password) VALUES (%s, %s, %s)", (username, email, hashed_pw))
                    conn.commit()
                    st.success("Registration successful! You can now log in.")
                cursor.close()
                conn.close()
            else:
                st.error("Please fill in all fields.")

def save_to_history(user_id, item, disposal_method):
    conn = connectToDB()
    cursor = conn.cursor()

    try:
        if disposal_method.lower() == 'trash':
            cursor.execute("INSERT INTO Trash (trash_ID, t_material, user_ID) VALUES (%s, %s, %s)", (None, item, user_id))
        
        elif disposal_method.lower() == 'recycle':
            cursor.execute("INSERT INTO Recycle (recycle_ID, r_material, user_ID) VALUES (%s, %s, %s)", (None, item, user_id))
            
        elif disposal_method.lower() == 'compost':
            cursor.execute("INSERT INTO Compost (compost_ID, c_material, user_ID) VALUES (%s, %s, %s)", (None, item, user_id))

        conn.commit()
        
    finally:
        cursor.close()
        conn.close()

def parse_ai_response(response_text):
    if ":" in response_text:
        item, method = response_text.split(":", 1)
        return item.strip(), method.strip()
    return response_text.strip(), ""

def get_user_id(email):
    conn = connectToDB()
    cursor = conn.cursor()
    cursor.execute("SELECT user_ID FROM USER WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_Recycle_Size(userID):
    conn = connectToDB()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Recycle WHERE user_ID = %s;", (userID,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_Compost_Size(userID):
    conn = connectToDB()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Compost WHERE user_ID = %s;", (userID,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_Trash_Size(userID):
    conn = connectToDB()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Trash WHERE user_ID = %s;", (userID,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# Main content (after login)
if authentication_status and "selected" in st.session_state:
    if st.session_state.selected == "Home":
        st.subheader("Revolutionizing Waste Sorting")
        st.image(
            "https://media.istockphoto.com/id/962933762/vector/ecology-and-waste-global-eco-friendly-plastic.jpg?s=612x612&w=0&k=20&c=RdbOw__qI_Vc0W8pU0dEiO9--Unfs-iXUEqQOCP-1HE=",
            width=400
        )

    elif st.session_state.selected == "Sort":
        st.subheader("Sort Waste into Trash, Recycle, or Compost")
        tab1, tab2 = st.tabs(["Text", "Image"])
        with tab1:
            user_input = st.text_input("Describe the waste you want to dispose:")

            if st.button("Sort", key="send_msg") and user_input:
                response_text = sort.get_gemini_response(user_input)
                st.write(response_text)
                st.session_state['last_response'] = response_text
                st.session_state['sort_clicked'] = True  # Set flag

        if 'last_response' in st.session_state and st.session_state.get('sort_clicked', False):
            if st.button("Save"):
                disposal_method, method = parse_ai_response(st.session_state['last_response'])
                user_id = get_user_id(email)
                if user_id and user_input and disposal_method:
                    save_to_history(user_id, user_input, disposal_method)
                    st.success("Saved to history!")
                else:
                    st.error("Could not save. Missing information.")

    elif st.session_state.selected == "History":
        st.subheader("View how much waste you have sorted")
        user_id = get_user_id(email)
        trashSize = get_Trash_Size(user_id)
        recycleSize = get_Recycle_Size(user_id)
        compostSize = get_Compost_Size(user_id)
        labels = ['Trash', 'Recycle', 'Compost']
        sizes = [trashSize, recycleSize, compostSize]

        fig = px.pie(
            values=sizes,
            names=labels,
            color=labels,  
            color_discrete_map={
                'Trash': 'orange',
                'Recycle': 'blue',
                'Compost': 'green'
            },
            title='Trash Sorted'
        )

        st.plotly_chart(fig)

