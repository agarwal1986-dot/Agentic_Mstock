import os
import requests
import hashlib
from dotenv import load_dotenv
from src import db

load_dotenv()
BASE_URL = "https://api.mstock.trade/openapi/typea"

def select_and_login(user_id, secret_key):
    """
    Select user by username, fetch credentials from DB,
    update .env, then run login + session flow.
    """
    # Fetch user credentials from DB
    user = db.get_user_credentials(user_id)
    if not user:
        raise ValueError("User not found in DB")

    # Update .env with selected user's credentials
    env_path = os.path.join(os.getcwd(), "config", ".env")
    lines = [
        f"DB_HOST=localhost\n",
        f"DB_USER=root\n",
        f"DB_PASSWORD=root\n",
        f"DB_NAME=mstock\n",
        f"DB_PORT=3306\n",
        f"M_STOCK_USER_ID={user['M_STOCK_USER_ID']}\n",
        f"M_STOCK_PASSWORD={user['M_STOCK_PASSWORD']}\n",
        f"M_STOCK_API_KEY={user['M_STOCK_API_KEY']}\n",
        f"M_STOCK_API_KEY_TYPE={user['M_STOCK_API_KEY_TYPE']}\n"
    ]
    with open(env_path, "w") as f:
        f.writelines(lines)

    # Step 1: Login
    url = f"{BASE_URL}/connect/login"
    headers = {
        'X-Mirae-Version': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'username': user['M_STOCK_USER_ID'],
        'password': user['M_STOCK_PASSWORD'],
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} {response.text}")

    result = response.json()
    otp = result.get("otp")
    request_token = result.get("request_token")

    # Save OTP + request_token in DB
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE MS01_API_Authentication_Credential
        SET M_STOCK_OTP = %s,
            M_STOCK_REQUEST_TOKEN = %s,
            SYS_UPDATE_DATE_TIME = CURRENT_TIMESTAMP
        WHERE M_STOCK_USER_ID = %s
    """, (otp, request_token, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    # Step 2: Generate Session
    checksum = hashlib.sha256((user['M_STOCK_API_KEY'] + request_token + secret_key).encode()).hexdigest()
    url = f"{BASE_URL}/session/token"
    headers = {
        'X-Mirae-Version': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'api_key': user['M_STOCK_API_KEY'],
        'request_token': request_token,
        'checksum': checksum,
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Session generation failed: {response.status_code} {response.text}")

    result = response.json()
    access_token = result.get("access_token")

    # Save access_token in DB
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE MS01_API_Authentication_Credential
        SET M_STOCK_ACCESS_TOKEN = %s,
            SYS_UPDATE_DATE_TIME = CURRENT_TIMESTAMP
        WHERE M_STOCK_USER_ID = %s
    """, (access_token, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    db.insert_log("INFO", f"Session generated for {user_id}", "user_login")
    return {"otp": otp, "request_token": request_token, "access_token": access_token}

# -------------------------------
# Interactive prompt
# -------------------------------
if __name__ == "__main__":
    user_id = input("Enter username to login: ")
    secret_key = input("Enter secret key: ")
    try:
        result = select_and_login(user_id, secret_key)
        print(f"Login flow complete: {result}")
    except Exception as e:
        print(f"Error: {e}")