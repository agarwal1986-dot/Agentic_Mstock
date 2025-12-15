from src import db

def delete_user(m_stock_user_id):
    """Delete a user entry from ms01_api_authentication_credential"""
    db.delete_credential(m_stock_user_id)
    db.insert_log("INFO", f"User {m_stock_user_id} deleted", "user_delete")

if __name__ == "__main__":
    m_stock_user_id = input("Enter M_STOCK_USER_ID to delete: ")
    delete_user(m_stock_user_id)
    print(f"User {m_stock_user_id} deleted successfully.")