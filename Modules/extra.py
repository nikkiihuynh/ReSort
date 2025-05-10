"""
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import sort
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import plotly.express as px
import pandas as pd
from PIL import Image

# --- Styling ---
st.markdown("""
#<style>
#@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
#html, body, [class*="css"] {
 #   font-family: 'Inter', sans-serif;
#}
#.title {
 #   position: relative;
 #   top: -70px;
 #   text-align: left;
#}
#</style>
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

        cursor.execute("""
INSERT INTO SortingHistory (user_ID, item, disposal_method) VALUES (%s, %s, %s) """, (user_id, item, disposal_method.lower()))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

def get_sorting_history(user_id):
    conn = connectToDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT item, disposal_method, sort_date
                   FROM SortingHistory
                   WHERE user_ID = %s
                   ORDER BY sort_date DESC
                   """, (user_id,))
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history

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
        # General static tips for all users
        st.markdown('### General Waste Disposal Tips')
        tips = [
            'Clean and dry recyclables before placing them in the bin to avoid contamination.',
            'Flatten cardboard boxes to save space in recycling bins.',
            'Check your local guidelines for accepted materials, as they vary by location.',
            'Avoid bagging recyclables in plastic bags; most facilities cannot process them.',
            'Keep a small compost bin in your kitchen for food scraps to reduce landfill waste.',
        ]
        for tip in tips:
            st.markdown(f'- {tip}')

        # Button to fetch personalized tips based on user history
        if st.button('Get personalized tips'):
            user_id = get_user_id(email)
            if user_id:
                history = get_sorting_history(user_id)
                if history:
                    tips_text = sort.get_targeted_tips(history)
                    st.subheader('Your Personalized Tips')
                    st.write(tips_text)
                else:
                    st.info('No sorting history available to generate personalized tips.')

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
                    disposal_method, explanation = parse_ai_response(st.session_state['last_response'])
                    valid_methods = ['trash', 'recycle', 'compost']
                    # Basic sanity checks
                    if (disposal_method.lower() in valid_methods
                        and user_input.strip()
                        and len(user_input.strip()) > 2):
                        user_id = get_user_id(email)
                        save_to_history(user_id, user_input, disposal_method)
                        st.success('Saved to history!')
                    else:
                        st.error('Cannot save: invalid input or disposal method')

        with tab2:
            image_file = st.file_uploader("Upload an image of an item", type=["jpg", "png", "jpeg"])
            if image_file is not None:
                img = Image.open(image_file)
                st.image(img, caption="Uploaded Image", use_column_width=True)

            if st.button("Analyze Image", key="analyze_image"):
                response_text = sort.get_sorting_from_image(img)
                st.write(response_text)
                st.session_state['last_response'] = response_text
                st.session_state['analyze_image_clicked'] = True

            if 'last_response' in st.session_state and st.session_state.get('analyze_image_clicked', False):
                user_input = st.session_state['last_response'].split('{')[1].split('}')[0]
                if st.button("Save Image"):
                    disposal_method, explanation = parse_ai_response(st.session_state['last_response'])
                    valid_methods = ['trash', 'recycle', 'compost']
                    # Basic sanity checks
                    if (disposal_method.lower() in valid_methods
                        and user_input.strip()
                        and len(user_input.strip()) > 2):
                        user_id = get_user_id(email)
                        save_to_history(user_id, user_input, disposal_method)
                        st.success('Saved to history!')
                    else:
                        st.error('Cannot save: invalid input or disposal method')
        
    elif st.session_state.selected == "History":
        st.subheader("View how much waste you have sorted")
        user_id = get_user_id(email)
        tab1, tab2 = st.tabs(["Statistics", "History"])
        with tab1:
            st.subheader("Statistics")
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

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total trashed items: ", trashSize)
            with col2:
                st.metric("Total recycled items: ", recycleSize)
            with col3:
                st.metric("Total composted items: ", compostSize)

        with tab2:
            st.subheader("History")
            history = get_sorting_history(user_id)
            if history:
                df = pd.DataFrame(history)
                df['sort_date'] = pd.to_datetime(df['sort_date']).dt.strftime('%m-%d-%Y %H:%M')
                df['disposal_method'] = df['disposal_method'].str.capitalize()

                df = df.rename(columns={
                    'item' : 'Item',
                    'disposal_method' : 'Disposal Method',
                    'sort_date' : 'Date Sorted'
                })

                def color_code(val):
                    colors = {
                        'Trash': '#F8D32B',
                        'Recycle': '#2154DC',
                        'Compost': '#1FAA21'
                    }
                    return f'background-color: {colors.get(val,"")}'

                st.dataframe(
                    df.style.applymap(color_code, subset=['Disposal Method']),
                    column_config ={
                        "Item": st.column_config.TextColumn("Item", width="medium"),
                        "Disposal Method": st.column_config.TextColumn("Disposal Method", width="medium"),
                        "Date Sorted": st.column_config.DatetimeColumn("Date Sorted", width="medium")
                    },
                    hide_index=True,
                    use_container_width=True,
                    height=400
                )
            else:
                st.info("No sorting history to display.")


"""