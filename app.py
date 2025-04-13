import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import sort

def connectToDB():
    return mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        password = 'password',
        database = 'resort'
    )

def register_user(email, password):
    conn = connectToDB()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM USER WHERE name = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        st.error("Email already registered. Please log in.")
    else:
        cursor.execute("INSERT INTO USER (name, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        st.success("Registration successful! You can now log in.")

    cursor.close()
    conn.close()

def login_user(email, password):
    conn = connectToDB()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM USER WHERE name =  %s AND password = %s", (email, password))
    existing_user = cursor.fetchone()
    if existing_user:
        st.success("Login Successful")
    else:
        st.error("Email or Password incorrect. Try Again.")
    
    cursor.close()
    conn.close()

#UI frontend code 

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .title {
        position: relative;
        top: -70px;  /* Adjust this value to move title higher */
        text-align: Left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="title">ReSort</h1>', unsafe_allow_html=True)

selected = option_menu(
    menu_title = None,
    options = ["Home", "Sort", "Login", "Register"],
    icons = ["house", "recycle", "key-fill", "key"],
    menu_icon = "list",
    orientation = "horizontal",
)

placeholder = st.empty()

if selected == "Home":
    st.subheader("Revolutionizing Waste Sorting")
    st.image("https://media.istockphoto.com/id/962933762/vector/ecology-and-waste-global-eco-friendly-plastic.jpg?s=612x612&w=0&k=20&c=RdbOw__qI_Vc0W8pU0dEiO9--Unfs-iXUEqQOCP-1HE=", width = 400)
if selected == "Sort":
    st.subheader("Sort Waste into Trash, Recycle, or Compost")
    user_input = st.text_input("Describe the waste you want to dispose:")

    if st.button("Sort", key="send_msg") and user_input:
        response_text = sort.get_chatgpt_response(user_input)
        st.write(response_text)

    with st.expander("History"):
        for msg in st.session_state['messages']:
            role = "You" if msg["role"] == "user" else "Assistant" if msg["role"] == "assistant" else "System"
            st.write(f"**{role}:** {msg['content']}")
if selected == "Login":
    with placeholder.form("login"):
        st.markdown("#### Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if email and password:
                login_user(email, password)
            else:
                st.error("Please make sure you fill out all fields")

if selected == "Register":
    with placeholder.form("Register"):
        st.markdown("#### Register")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        if submit:
            if email and password:
                register_user(email, password)
            else:
                st.error("Please make sure you fill out all fields")



