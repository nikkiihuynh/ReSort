import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='password',
        database='resort'
    )

def fetch_users_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, password, email FROM USER")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    credentials = {'usernames': {}}
    for name, password, email in users:
        credentials['usernames'][email] = {
            'name': name,
            'password': password,
            'email': email,
            'roles': []
        }
    return credentials

def insert_user(name, email, hashed_password):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO USER (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

def user_exists(email):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def get_user_id(email):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_ID FROM USER WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def save_to_history(user_id, item, disposal_method):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        if disposal_method.lower() == 'trash':
            cursor.execute("INSERT INTO Trash (trash_ID, t_material, user_ID) VALUES (%s, %s, %s)", (None, item, user_id))
        
        elif disposal_method.lower() == 'recycle':
            cursor.execute("INSERT INTO Recycle (recycle_ID, r_material, user_ID) VALUES (%s, %s, %s)", (None, item, user_id))
            
        elif disposal_method.lower() == 'compost':
            cursor.execute("INSERT INTO Compost (compost_ID, c_material, user_ID) VALUES (%s, %s, %s)", (None, item, user_id))

        cursor.execute("""INSERT INTO SortingHistory (user_ID, item, disposal_method) VALUES (%s, %s, %s) """, (user_id, item, disposal_method))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

def get_Recycle_Size(userID):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Recycle WHERE user_ID = %s;", (userID,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_Compost_Size(userID):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Compost WHERE user_ID = %s;", (userID,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_Trash_Size(userID):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Trash WHERE user_ID = %s;", (userID,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_sorting_history(user_id):
    conn = connect_to_db()
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

