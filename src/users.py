from src import db

def add_user(user_id, password, api_key, api_key_type):
    """Add a new user"""
    db.insert_credential(user_id, password, api_key, api_key_type)
    db.insert_log("INFO", f"User {user_id} added", "users_api")

def update_user(user_id, password=None, api_key=None, api_key_type=None):
    """Update user details (username not editable)"""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE MS01_API_Authentication_Credential
        SET M_STOCK_PASSWORD = COALESCE(%s, M_STOCK_PASSWORD),
            M_STOCK_API_KEY = COALESCE(%s, M_STOCK_API_KEY),
            M_STOCK_API_KEY_TYPE = COALESCE(%s, M_STOCK_API_KEY_TYPE),
            SYS_UPDATE_DATE_TIME = CURRENT_TIMESTAMP
        WHERE M_STOCK_USER_ID = %s
    """, (password, api_key, api_key_type, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    db.insert_log("INFO", f"User {user_id} updated", "users_api")

def delete_user(user_id):
    """Delete a user entry"""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MS01_API_Authentication_Credential WHERE M_STOCK_USER_ID = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    db.insert_log("INFO", f"User {user_id} deleted", "users_api")