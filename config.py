import os
import sys
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from src import db

# Load environment variables
load_dotenv()

# -------------------------------
# Encryption Key Management
# -------------------------------

def get_encryption_key(key_id: int = None) -> str:
    """
    Fetch encryption key.
    Priority:
    1. Specific KEY_ID from SEC01_ENCRYPTION_KEY (if provided)
    2. Active key ID from .env (ENCRYPTION_KEY_ID)
    3. Latest key from SEC01_ENCRYPTION_KEY
    4. .env fallback (ENCRYPTION_KEY)
    """
    try:
        if key_id:
            row = db.fetch_one("SELECT ENCRYPTION_KEY FROM SEC01_ENCRYPTION_KEY WHERE KEY_ID=%s", (key_id,))
            if row and row.get("ENCRYPTION_KEY"):
                return row["ENCRYPTION_KEY"]

        env_key_id = os.getenv("ENCRYPTION_KEY_ID")
        if env_key_id:
            row = db.fetch_one("SELECT ENCRYPTION_KEY FROM SEC01_ENCRYPTION_KEY WHERE KEY_ID=%s", (env_key_id,))
            if row and row.get("ENCRYPTION_KEY"):
                return row["ENCRYPTION_KEY"]

        row = db.fetch_one("SELECT ENCRYPTION_KEY FROM SEC01_ENCRYPTION_KEY ORDER BY KEY_ID DESC LIMIT 1")
        if row and row.get("ENCRYPTION_KEY"):
            return row["ENCRYPTION_KEY"]
    except Exception:
        pass

    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise RuntimeError("ENCRYPTION_KEY is missing. Set it in DB or .env")
    return key

def encrypt_str(plain: str) -> str:
    """Encrypt using the active key"""
    key = get_encryption_key()
    fernet = Fernet(key.encode())
    return fernet.encrypt(plain.encode()).decode()

def decrypt_str(cipher: str, key_id: int = None) -> str:
    """
    Decrypt using the provided key_id.
    If key_id is missing or fails, try all known keys.
    """
    try:
        key = get_encryption_key(key_id)
        fernet = Fernet(key.encode())
        return fernet.decrypt(cipher.encode()).decode()
    except Exception:
        # fallback: try all keys
        rows = db.fetch_all("SELECT ENCRYPTION_KEY FROM SEC01_ENCRYPTION_KEY ORDER BY KEY_ID DESC")
        for row in rows:
            try:
                fernet = Fernet(row["ENCRYPTION_KEY"].encode())
                return fernet.decrypt(cipher.encode()).decode()
            except Exception:
                continue
        raise ValueError("Unable to decrypt with any known key")

# -------------------------------
# Login / Logout Flow (unchanged)
# -------------------------------

def login(user_id: str):
    print("Step 1: Fetching credentials from DB...")
    creds = db.fetch_credentials(user_id)
    if not creds:
        print("❌ Failed to fetch credentials")
        return None
    print("✅ Credentials fetched successfully")

    print("Step 2: Sending login request to mStock...")
    login_response = send_login_request(creds)
    print(f"DEBUG: Full login JSON: {login_response}")

    if login_response.get("status") != "success":
        print("❌ Login failed")
        return None

    request_token = input("Enter 3-digit OTP (request token): ").strip()
    print(f"DEBUG: Using request_token: {request_token}")

    print("Step 3: Generating session...")
    session = generate_session(login_response, request_token)
    print(f"DEBUG: Full session JSON: {session}")

    if session.get("status") != "success":
        print("❌ Session generation failed")
        return None
    print("✅ Session generated successfully")

    print("Step 4: Updating DB with new tokens + OTP...")
    update_success = db.update_credential(
        user_id=user_id,
        access_token=session["data"]["access_token"],
        refresh_token=session["data"]["refresh_token"],
        enctoken=session["data"]["enctoken"],
        login_time=session["data"]["login_time"]
    )

    if update_success:
        print("✅ DB updated successfully with new tokens")
    else:
        print("❌ Failed to update DB with new tokens")

    log_success = db.log_request_response(
        api_name="login_session",
        request_json={"user_id": user_id, "request_token": request_token},
        response_json=session
    )

    if log_success:
        print("✅ Request/Response logged successfully")
    else:
        print("❌ Failed to log Request/Response")

    return session

def logout(user_id: str):
    confirm = input("Are you sure you want to logout? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Logout cancelled")
        return False

    print("Step 1: Sending logout request to mStock...")
    logout_response = send_logout_request(user_id)
    print(f"DEBUG: Full logout JSON: {logout_response}")

    if logout_response.get("status") != "success":
        print("❌ Logout failed")
        return False
    print("✅ Logout successful")

    log_success = db.log_request_response(
        api_name="logout_session",
        request_json={"user_id": user_id},
        response_json=logout_response
    )

    if log_success:
        print("✅ Logout Request/Response logged successfully")
    else:
        print("❌ Failed to log Logout Request/Response")

    return True

def send_login_request(creds: dict) -> dict:
    return {"status": "success", "data": {"ugid": "dummy-ugid", "cid": creds.get("cid"), "nm": creds.get("nm")}}

def generate_session(login_response: dict, request_token: str) -> dict:
    return {"status": "success", "data": {"user_id": "dummy-user", "access_token": "dummy-access-token",
                                          "refresh_token": "dummy-refresh-token", "enctoken": "dummy-enctoken",
                                          "login_time": "2025-12-14 03:50:43"}}

def send_logout_request(user_id: str) -> dict:
    return {"status": "success", "data": {"user_id": user_id, "logout_time": "2025-12-14 03:55:00"}}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "logout":
        user_id = input("Enter your mStock User ID: ").strip()
        logout(user_id)
    else:
        user_id = input("Enter your mStock User ID: ").strip()
        login(user_id)