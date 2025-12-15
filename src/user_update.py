from src import db
from getpass import getpass

def update_user(
    m_stock_user_id,
    m_stock_password=None,
    m_stock_api_key=None,
    m_stock_api_key_type=None
):
    """
    Update user details (M_STOCK_USER_ID not editable, tokens are logged separately).
    If password is updated, db.update_credential will also update ENCRYPTION_KEY_ID.
    """
    try:
        db.update_credential(
            m_stock_user_id,
            password=m_stock_password,
            api_key=m_stock_api_key,
            api_key_type=m_stock_api_key_type
        )
        db.insert_log("INFO", f"User {m_stock_user_id} updated", "user_update")
        print(f"✅ User {m_stock_user_id} updated successfully.")
    except Exception as e:
        print(f"❌ Failed to update user {m_stock_user_id}: {e}")

if __name__ == "__main__":
    m_stock_user_id = input("Enter M_STOCK_USER_ID to update: ").strip()
    # Masked password input for security
    m_stock_password = getpass("Enter new M_STOCK_PASSWORD (or press Enter to skip): ").strip() or None
    m_stock_api_key = input("Enter new M_STOCK_API_KEY (or press Enter to skip): ").strip() or None
    m_stock_api_key_type = input("Enter new M_STOCK_API_KEY_TYPE (A/B or press Enter to skip): ").strip().upper() or None

    update_user(
        m_stock_user_id,
        m_stock_password,
        m_stock_api_key,
        m_stock_api_key_type
    )