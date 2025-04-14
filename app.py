import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector

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

## TODO: save user waste history
def save_to_history(user_id, item, disposal_method):
    conn = connectToDB()
    cursor = conn.cursor()

    try:
        if disposal_method.lower() == 'trash':
            cursor.execute("INSERT INTO Trash (t_material) VALUES (%s)", (item,))
            trash_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO Sorted (user_ID, trash_ID)
                VALUES (%s, %s)""", (user_id, trash_id))
        
        elif disposal_method.lower() == 'recycle':
            cursor.execute("INSERT INTO Recycle (r_material) VALUES (%s)", (item,))
            recycle_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO Sorted (user_ID, recycle_ID)
                VALUES (%s, %s)""", (user_id, recycle_id))
            
        elif disposal_method.lower() == 'compost':
            cursor.execute("INSERT INTO Compost (c_material) VALUES (%s)", (item,))
            compost_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO Sorted (user_ID, compost_ID)
                VALUES (%s, %s)""", (user_id, compost_id))

        conn.commit()
        
    finally:
        cursor.close()
        conn.close()

## TODO: Make user history accessible to the user





#UI frontend code 

st.markdown(
    """
    <style>
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
    options = ["Home", "Login", "Register"],
    icons = ["house", "key-fill", "key"],
    menu_icon = "list",
    orientation = "horizontal",
)

placeholder = st.empty()

if selected == "Home":
    st.subheader("Revolutionizing Waste Sorting")
    st.image("https://media.istockphoto.com/id/962933762/vector/ecology-and-waste-global-eco-friendly-plastic.jpg?s=612x612&w=0&k=20&c=RdbOw__qI_Vc0W8pU0dEiO9--Unfs-iXUEqQOCP-1HE=", width = 400)
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



