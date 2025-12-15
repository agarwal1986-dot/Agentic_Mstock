import os
import requests
import hashlib
from dotenv import load_dotenv
from src import db

load_dotenv()

BASE_URL = "https://api.mstock.trade/openapi/typea"

# -------------------------------
# Step 1: Login
# -------------------------------
def login(user_id):
    """
    Login to mStock API using username/password.
    Stores OTP + request_token in DB.
    """
    url = f"{BASE_URL}/connect/login"
    headers = {
        'X-Mirae-Version': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'username': os.getenv("M_STOCK_USER_ID"),
        'password': os.getenv("M_STOCK_PASSWORD"),
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

    db.insert_log("INFO", f"Login successful for {user_id}", "auth_api")
    return otp, request_token

# -------------------------------
# Step 2: Generate Session
# -------------------------------
def generate_session(user_id, api_key, request_token, secret_key):
    """
    Generate session token using api_key + request_token + checksum.
    Stores access_token in DB.
    """
    checksum = hashlib.sha256((api_key + request_token + secret_key).encode()).hexdigest()

    url = f"{BASE_URL}/session/token"
    headers = {
        'X-Mirae-Version': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'api_key': api_key,
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

    db.insert_log("INFO", f"Session generated for {user_id}", "auth_api")
    return access_token

# -------------------------------
# Step 3: Verify TOTP (if enabled)
# -------------------------------
def verify_totp(api_key, otp, access_token):
    url = f"{BASE_URL}/session/verifytotp"
    headers = {
        'X-Mirae-Version': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'api_key': api_key,
        'otp': otp,
        'access_token': access_token,
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"TOTP verification failed: {response.status_code} {response.text}")

    return response.json()

# -------------------------------
# Step 4: Fund Summary
# -------------------------------
def get_fund_summary(api_key, access_token):
    url = f"{BASE_URL}/user/fundsummary"
    headers = {
        'X-Mirae-Version': '1',
        'Authorization': f"token {api_key}:{access_token}",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Fund summary failed: {response.status_code} {response.text}")

    return response.json()

# -------------------------------
# Step 5: Logout
# -------------------------------
def logout(api_key, access_token):
    url = f"{BASE_URL}/logout"
    headers = {
        'X-Mirae-Version': '1',
        'Authorization': f"token {api_key}:{access_token}",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Logout failed: {response.status_code} {response.text}")

    db.insert_log("INFO", "User logged out", "auth_api")
    return response.json()