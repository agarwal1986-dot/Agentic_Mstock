import sys
import os

# Add src folder to sys.path so we can import modules from it
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from user_add import add_user
from user_update import update_user
from user_delete import delete_user
import db


def menu():
    print("\n=== MStock API Authentication Flow Menu ===")
    print("1. Add User")
    print("2. Update User")
    print("3. Delete User")
    print("4. Run All (Add → Update → Delete)")
    print("5. Exit")
    print("6. View Logs")

def run_add():
    print("\n[STEP 1] Adding a new user...")
    m_stock_user_id = input("Enter M_STOCK_USER_ID: ")
    m_stock_password = input("Enter M_STOCK_PASSWORD: ")
    m_stock_api_key = input("Enter M_STOCK_API_KEY: ")
    m_stock_api_key_type = input("Enter M_STOCK_API_KEY_TYPE (A/B): ").strip().upper()

    add_user(m_stock_user_id, m_stock_password, m_stock_api_key, m_stock_api_key_type)
    print(f"[INFO] User '{m_stock_user_id}' added successfully.\n")

def run_update():
    print("\n[STEP 2] Updating user details...")
    m_stock_user_id = input("Enter M_STOCK_USER_ID to update: ")
    m_stock_password = input("Enter new M_STOCK_PASSWORD (or press Enter to skip): ") or None
    m_stock_api_key = input("Enter new M_STOCK_API_KEY (or press Enter to skip): ") or None
    m_stock_api_key_type = input("Enter new M_STOCK_API_KEY_TYPE (A/B or press Enter to skip): ").strip().upper() or None
    m_stock_request_token = input("Enter new M_STOCK_REQUEST_TOKEN (or press Enter to skip): ") or None
    m_stock_access_token = input("Enter new M_STOCK_ACCESS_TOKEN (or press Enter to skip): ") or None
    m_stock_otp = input("Enter new M_STOCK_OTP (or press Enter to skip): ") or None

    update_user(
        m_stock_user_id,
        m_stock_password,
        m_stock_api_key,
        m_stock_api_key_type,
        m_stock_request_token,
        m_stock_access_token,
        m_stock_otp
    )
    print(f"[INFO] User '{m_stock_user_id}' updated successfully.\n")

def run_delete():
    print("\n[STEP 3] Deleting user...")
    m_stock_user_id = input("Enter M_STOCK_USER_ID to delete: ")
    delete_user(m_stock_user_id)
    print(f"[INFO] User '{m_stock_user_id}' deleted successfully.\n")

def run_all():
    print("\n[STEP 4] Running full flow (Add → Update → Delete)...")
    run_add()
    run_update()
    run_delete()
    print("[INFO] Full flow completed.\n")

def view_logs():
    print("\n[STEP 6] Viewing recent logs...")
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT LOG_LEVEL, LOG_MESSAGE, SOURCE_MODULE, TIMESTAMP
        FROM logs
        ORDER BY TIMESTAMP DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("[INFO] No logs found.\n")
    else:
        for row in rows:
            print(f"[{row['LOG_LEVEL']}] {row['LOG_MESSAGE']} "
                  f"(Source: {row['SOURCE_MODULE']}, Time: {row['TIMESTAMP']})")
        print("\n[INFO] Displayed latest 10 logs.\n")

def main():
    while True:
        menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            run_add()
        elif choice == "2":
            run_update()
        elif choice == "3":
            run_delete()
        elif choice == "4":
            run_all()
        elif choice == "5":
            print("\nExiting... Goodbye!")
            break
        elif choice == "6":
            view_logs()
        else:
            print("[ERROR] Invalid choice. Please select 1-6.\n")

if __name__ == "__main__":
    main()