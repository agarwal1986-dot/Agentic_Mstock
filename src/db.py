import mysql.connector
import os
from dotenv import load_dotenv
import config   # <-- import config to use encrypt_str / decrypt_str
import secrets
import string

# Load environment variables from .env
load_dotenv()

def get_connection():
    """Establish a connection to the MySQL database using .env values"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "mstock"),
        port=int(os.getenv("DB_PORT", 3306))
    )

# -------------------------------
# Credential Operations
# -------------------------------

def insert_credential(user_id, password, api_key, api_key_type="A"):
    """Insert a new credential record with encryption key tracking"""
    conn = get_connection()
    cursor = conn.cursor()

    # Encrypt password before storing
    encrypted_password = config.encrypt_str(password)

    # Get active key ID from .env or fallback to latest DB key
    active_key_id = os.getenv("ENCRYPTION_KEY_ID")
    if not active_key_id:
        cursor.execute("SELECT KEY_ID FROM SEC01_ENCRYPTION_KEY ORDER BY KEY_ID DESC LIMIT 1")
        row = cursor.fetchone()
        active_key_id = row[0] if row else None

    cursor.execute("""
        INSERT INTO MS01_API_Authentication_Credential
        (M_STOCK_USER_ID, M_STOCK_PASSWORD, M_STOCK_API_KEY, M_STOCK_API_KEY_TYPE, ENCRYPTION_KEY_ID)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, encrypted_password, api_key, api_key_type, active_key_id))

    conn.commit()
    cursor.close()
    conn.close()

def update_credential(user_id, password=None, api_key=None, api_key_type=None):
    """Update static credential details (tokens are no longer stored here)"""
    conn = get_connection()
    cursor = conn.cursor()

    # Encrypt password if provided
    encrypted_password = config.encrypt_str(password) if password else None

    # Get active key ID if password is updated
    active_key_id = None
    if password:
        active_key_id = os.getenv("ENCRYPTION_KEY_ID")
        if not active_key_id:
            cursor.execute("SELECT KEY_ID FROM SEC01_ENCRYPTION_KEY ORDER BY KEY_ID DESC LIMIT 1")
            row = cursor.fetchone()
            active_key_id = row[0] if row else None

    cursor.execute("""
        UPDATE MS01_API_Authentication_Credential
        SET M_STOCK_PASSWORD = COALESCE(%s, M_STOCK_PASSWORD),
            M_STOCK_API_KEY = COALESCE(%s, M_STOCK_API_KEY),
            M_STOCK_API_KEY_TYPE = COALESCE(%s, M_STOCK_API_KEY_TYPE),
            ENCRYPTION_KEY_ID = COALESCE(%s, ENCRYPTION_KEY_ID),
            SYS_UPDATE_DATE_TIME = CURRENT_TIMESTAMP
        WHERE M_STOCK_USER_ID = %s
    """, (encrypted_password, api_key, api_key_type, active_key_id, user_id))

    conn.commit()
    cursor.close()
    conn.close()

def delete_credential(user_id):
    """Delete a credential record"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MS01_API_Authentication_Credential WHERE M_STOCK_USER_ID = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_latest_credential():
    """Fetch the most recently updated credential"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("""
        SELECT M_STOCK_USER_ID, M_STOCK_PASSWORD, M_STOCK_API_KEY, M_STOCK_API_KEY_TYPE, ENCRYPTION_KEY_ID
        FROM MS01_API_Authentication_Credential
        ORDER BY SYS_UPDATE_DATE_TIME DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row and row.get("M_STOCK_PASSWORD"):
        try:
            row["M_STOCK_PASSWORD"] = config.decrypt_str(row["M_STOCK_PASSWORD"], row.get("ENCRYPTION_KEY_ID"))
        except Exception:
            row["M_STOCK_PASSWORD"] = None
    return row

def get_user_credentials(user_id):
    """Fetch credentials for a specific user by ID.
    Returns both ciphertext and decrypted password for testing/debugging.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("""
        SELECT M_STOCK_USER_ID, M_STOCK_PASSWORD, M_STOCK_API_KEY, M_STOCK_API_KEY_TYPE, ENCRYPTION_KEY_ID
        FROM MS01_API_Authentication_Credential
        WHERE M_STOCK_USER_ID = %s
    """, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and user.get("M_STOCK_PASSWORD"):
        # Preserve ciphertext separately
        user["M_STOCK_PASSWORD_CIPHERTEXT"] = user["M_STOCK_PASSWORD"]
        try:
            # Add decrypted value separately
            user["M_STOCK_PASSWORD_DECRYPTED"] = config.decrypt_str(
                user["M_STOCK_PASSWORD"], user.get("ENCRYPTION_KEY_ID")
            )
        except Exception:
            user["M_STOCK_PASSWORD_DECRYPTED"] = None
    return user

def get_all_users():
    """Fetch all usernames (for dropdowns in GUI)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT M_STOCK_USER_ID FROM MS01_API_Authentication_Credential")
    users = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return users

# -------------------------------
# Logging Operations
# -------------------------------

def insert_log(level, message, source_module=None):
    """Insert a simple log entry into generic logs table"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (LOG_LEVEL, LOG_MESSAGE, SOURCE_MODULE)
        VALUES (%s, %s, %s)
    """, (level, message, source_module))
    conn.commit()
    cursor.close()
    conn.close()

def insert_request_response_log(
    log_level,
    message,
    module,
    request=None,
    response=None,
    api_name=None,
    login_seq_id=None
):
    """
    Insert a detailed request/response log entry into MS01_REQUEST_RESPONSE_LOG.
    If login_seq_id is not provided, generate a new one.
    """
    try:
        if not login_seq_id:
            login_seq_id = generate_login_seq_id()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MS01_REQUEST_RESPONSE_LOG 
            (log_level, message, module, request, response, api_name, login_seq_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (log_level, message, module, request, response, api_name, login_seq_id))
        conn.commit()
    except Exception as e:
        try:
            cursor.execute("""
                INSERT INTO MS01_REQUEST_RESPONSE_LOG 
                (log_level, message, module, request, response, api_name, login_seq_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, ("ERROR", f"Logging failed: {message}", module, request, str(e), api_name, login_seq_id))
            conn.commit()
        except Exception as inner_e:
            print("Critical DB Logging Error:", inner_e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------------
# Response Data Update Helper
# -------------------------------

def update_auth_credentials(user_id: str, login_json: dict, session_json: dict) -> bool:
    """Update MS01_API_Authentication_Credential with values from login/session JSON"""
    try:
        login_data = login_json.get("data", {})
        session_data = session_json.get("data", {})

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE MS01_API_Authentication_Credential
            SET
                M_CLIENT_CODE        = COALESCE(%s, M_CLIENT_CODE),
                M_RESPONSE_USER_ID   = COALESCE(%s, M_RESPONSE_USER_ID),
                M_RESPONSE_USER_NAME = COALESCE(%s, M_RESPONSE_USER_NAME),
                M_ACCESS_TOKEN       = COALESCE(%s, M_ACCESS_TOKEN),
                M_PUBLIC_TOKEN       = COALESCE(%s, M_PUBLIC_TOKEN),
                M_REFRESH_TOKEN      = COALESCE(%s, M_REFRESH_TOKEN),
                M_ENC_TOKEN          = COALESCE(%s, M_ENC_TOKEN),
                LAST_LOGIN_DATE      = COALESCE(%s, LAST_LOGIN_DATE),
                LAST_LOGOUT_DATE     = COALESCE(%s, LAST_LOGOUT_DATE)
            WHERE M_STOCK_USER_ID = %s
        """, (
            login_data.get("cid"),
            session_data.get("user_id"),
            session_data.get("user_name"),
            session_data.get("access_token"),
            session_data.get("public_token"),
            session_data.get("refresh_token"),
            session_data.get("enctoken"),
            session_data.get("login_time"),
            session_data.get("logout_time"),
            user_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"DB update failed: {e}")
        return False
    
    # -------------------------------
# Helper: Generate Complex Login Sequence ID
# -------------------------------

def generate_unique_seq_id(table: str, column: str, length: int = 20) -> str:
    """
    Generate a unique, complex sequence ID with numbers, alphabets, and special characters.
    Ensures uniqueness by checking the given table/column in DB.
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        candidate = ''.join(secrets.choice(alphabet) for _ in range(length))
        cursor.execute(f"SELECT 1 FROM {table} WHERE {column} = %s LIMIT 1", (candidate,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return candidate

# -------------------------------
# Logging Operations
# -------------------------------

def insert_log(level, message, source_module=None):
    """Insert a simple log entry into generic logs table"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (LOG_LEVEL, LOG_MESSAGE, SOURCE_MODULE)
        VALUES (%s, %s, %s)
    """, (level, message, source_module))
    conn.commit()
    cursor.close()
    conn.close()

