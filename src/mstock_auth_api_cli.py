"""
mStock Authentication CLI
Handles login/logout flows with proper encryption/decryption of credentials
and consistent logging with unique login_seq_id.
"""

import argparse
import os

from src import db
import config
from tradingapi_a.mconnect import MConnect


def login(user_id: str):
    # Step 1: Fetch credentials
    print("Step 1: Fetching credentials from DB...")
    creds = db.get_user_credentials(user_id)
    if not creds:
        return {"status": "failure", "reason": "User not found in DB"}
    print("✅ Credentials fetched successfully")

    # Generate unique login_seq_id for this flow
    login_seq_id = db.generate_unique_seq_id("MS01_REQUEST_RESPONSE_LOG", "login_seq_id")
  #  print("DEBUG: Generated LOGIN_SEQ_ID:", login_seq_id)

    # Decrypt password before using
    try:
        decrypted_password = config.decrypt_str(
            creds["M_STOCK_PASSWORD_CIPHERTEXT"], creds["ENCRYPTION_KEY_ID"]
        )
    except Exception as e:
        return {"status": "failure", "reason": f"Password decryption failed: {e}"}

    mconnect_obj = MConnect()

    # Step 2: Login request
    print("Step 2: Sending login request to mStock...")
    try:
        login_response = mconnect_obj.login(user_id, decrypted_password)
        try:
            login_json = login_response.json() if hasattr(login_response, "json") else login_response
        except Exception as parse_err:
            login_json = {"error": f"JSON parse failed: {str(parse_err)}"}

        db.insert_request_response_log(
            "INFO", "Login call completed", "mstock_auth_api_cli",
            str({"user_id": user_id}), str(login_json),
            api_name="login", login_seq_id=login_seq_id
        )
    #    print("DEBUG: Full login JSON:", login_json)
    except Exception as e:
        db.insert_request_response_log(
            "ERROR", "Login call failed", "mstock_auth_api_cli",
            str({"user_id": user_id}), str(e),
            api_name="login", login_seq_id=login_seq_id
        )
        return {"status": "failure", "reason": str(e)}

    # Step 3: OTP prompt
    request_token = input("Enter 3-digit OTP (request token): ").strip()
   # print("DEBUG: Using request_token:", request_token)

    # Step 4: Generate session
    print("Step 4: Generating session...")
    try:
        session_response = mconnect_obj.generate_session(
            creds["M_STOCK_API_KEY"], request_token, ""
        )
        try:
            session_json = session_response.json() if hasattr(session_response, "json") else session_response
        except Exception as parse_err:
            session_json = {"error": f"JSON parse failed: {str(parse_err)}"}

        db.insert_request_response_log(
            "INFO", "Generate session call completed", "mstock_auth_api_cli",
            str({"api_key": creds["M_STOCK_API_KEY"], "request_token": request_token}),
            str(session_json), api_name="generate_session", login_seq_id=login_seq_id
        )
    #   print("DEBUG: Full session JSON:", session_json)
    except Exception as e:
        db.insert_request_response_log(
            "ERROR", "Generate session failed", "mstock_auth_api_cli",
            str({"api_key": creds["M_STOCK_API_KEY"], "request_token": request_token}),
            str(e), api_name="generate_session", login_seq_id=login_seq_id
        )
        return {"status": "failure", "reason": str(e)}

    if not session_json or "error" in session_json:
        return {"status": "failure", "reason": session_json.get("error", "Session generation failed")}
    print("✅ Session generated successfully")

    # Step 5: Update .env file
    print("Step 5: Updating .env file with latest values...")
    update_env({
        "M_STOCK_USER_ID": user_id,
        "M_STOCK_PASSWORD": creds["M_STOCK_PASSWORD_CIPHERTEXT"],  # store ciphertext only
        "M_STOCK_API_KEY": creds["M_STOCK_API_KEY"],
        "M_STOCK_API_KEY_TYPE": "A",
        "M_STOCK_REQUEST_TOKEN_OTP": request_token,
        "M_STOCK_ACCESS_TOKEN": session_json.get("data", {}).get("access_token"),
        "M_STOCK_CLIENT_CODE": login_json.get("data", {}).get("cid"),
        "M_STOCK_RESPONSE_USER_ID": session_json.get("data", {}).get("user_id"),
        "M_STOCK_RESPONSE_USER_NAME": session_json.get("data", {}).get("user_name"),
        "M_STOCK_PUBLIC_TOKEN": session_json.get("data", {}).get("public_token"),
        "M_STOCK_REFRESH_TOKEN": session_json.get("data", {}).get("refresh_token"),
        "M_STOCK_ENC_TOKEN": session_json.get("data", {}).get("enctoken"),
        "M_STOCK_LAST_LOGIN_DATE": session_json.get("data", {}).get("login_time"),
        "M_STOCK_LAST_LOGOUT_DATE": session_json.get("data", {}).get("logout_time")
    })
    print("✅ .env file updated")

    # Step 6: Update DB
    print("Step 6: Updating DB table with response values...")
    db.update_auth_credentials(user_id, login_json, session_json)
    print("✅ DB table updated")

    db.insert_request_response_log(
        "INFO", "Login flow completed successfully", "mstock_auth_api_cli",
        str({"user_id": user_id}), str(session_json),
        api_name="login", login_seq_id=login_seq_id
    )

    return {
        "status": "success",
        "message": "Login successful",
        "tokens": {
            "request_token": request_token,
            "access_token": session_json.get("data", {}).get("access_token"),
            "login_seq_id": login_seq_id
        }
    }


def logout(user_id: str):
    print("Logging out...")
    login_seq_id = db.generate_unique_seq_id("MS01_REQUEST_RESPONSE_LOG", "login_seq_id")
    try:
        update_env({
            "M_STOCK_REQUEST_TOKEN_OTP": "",
            "M_STOCK_ACCESS_TOKEN": "",
            "M_STOCK_CLIENT_CODE": "",
            "M_STOCK_RESPONSE_USER_ID": "",
            "M_STOCK_RESPONSE_USER_NAME": "",
            "M_STOCK_PUBLIC_TOKEN": "",
            "M_STOCK_REFRESH_TOKEN": "",
            "M_STOCK_ENC_TOKEN": "",
            "M_STOCK_LAST_LOGIN_DATE": "",
            "M_STOCK_LAST_LOGOUT_DATE": ""
        })

        db.insert_request_response_log(
            "INFO", "Logout call completed", "mstock_auth_api_cli",
            str({"user_id": user_id}), "{}", api_name="logout", login_seq_id=login_seq_id
        )
        return {"status": "success", "message": "Logout successful", "login_seq_id": login_seq_id}
    except Exception as e:
        db.insert_request_response_log(
            "ERROR", "Logout failed", "mstock_auth_api_cli",
            str({"user_id": user_id}), str(e), api_name="logout", login_seq_id=login_seq_id
        )
        return {"status": "failure", "reason": str(e), "login_seq_id": login_seq_id}


def update_env(updates: dict):
    """Update .env file with new values"""
    env_path = ".env"
    if not os.path.exists(env_path):
        return

    with open(env_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        key = line.split("=")[0].strip()
        if key in updates:
            new_lines.append(f"{key}={updates[key]}\n")
        else:
            new_lines.append(line)

    for key, value in updates.items():
        if not any(l.startswith(f"{key}=") for l in new_lines):
            new_lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mStock Auth CLI")
    parser.add_argument("action", choices=["login", "logout"], nargs="?", default="login")
    args = parser.parse_args()

    user_id = input("Enter your mStock User ID: ").strip()

    if args.action == "login":
        result = login(user_id)
    elif args.action == "logout":
        confirm = input("Are you sure you want to logout? (y/n): ").strip().lower()
        if confirm == "y":
            result = logout(user_id)
        else:
            db.insert_request_response_log(
                "INFO", "Logout cancelled by user", "mstock_auth_api_cli",
                str({"user_id": user_id}), "{}", api_name="logout"
            )
            result = {"status": "failure", "reason": "Logout cancelled by user"}

    if result["status"] == "success":
        print(f"✅ SUCCESS: {result.get('message')}")
        if "tokens" in result:
            print(f"Request Token: {result['tokens'].get('request_token')}")
            print(f"Access Token: {result['tokens'].get('access_token')}")
            print(f"Login Seq ID: {result['tokens'].get('login_seq_id')}")
    else:
        print(f"❌ FAILURE: {result.get('reason')}")

