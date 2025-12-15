from src import db
from getpass import getpass

def add_user(m_stock_user_id, m_stock_password, m_stock_api_key, m_stock_api_key_type="A"):
    """Add a new user into MS01_API_Authentication_Credential (static fields only)"""
    try:
        # db.insert_credential will encrypt the password internally
        db.insert_credential(
            m_stock_user_id,
            m_stock_password,
            m_stock_api_key,
            m_stock_api_key_type
        )
        db.insert_log("INFO", f"User {m_stock_user_id} added", "user_add")
        print(f"✅ User {m_stock_user_id} added successfully.")
    except Exception as e:
        print(f"❌ Failed to add user {m_stock_user_id}: {e}")

if __name__ == "__main__":
    m_stock_user_id = input("Enter M_STOCK_USER_ID: ").strip()
    # Masked password input
    m_stock_password = getpass("Enter M_STOCK_PASSWORD: ").strip()
    m_stock_api_key = input("Enter M_STOCK_API_KEY: ").strip()
    m_stock_api_key_type = input("Enter M_STOCK_API_KEY_TYPE (A/B): ").strip().upper() or "A"

    add_user(m_stock_user_id, m_stock_password, m_stock_api_key, m_stock_api_key_type)