"""
Test script for verifying encryption/decryption round-trip.
Located under src/tests for safe separation from production code.
"""

from src import db

def test_encryption(m_stock_user_id, plain_password=None):
    """
    Fetch stored credentials for a user and test decryption.
    Prints both ciphertext and decrypted password.
    If plain_password is provided, compare with decrypted value.
    """
    print("\n--- Test encryption/decryption ---")
    try:
        creds = db.get_user_credentials(m_stock_user_id)
        if not creds:
            print("❌ No credentials found for user.")
            return

        # Print both ciphertext and decrypted values
        print(f"Stored ciphertext: {creds.get('M_STOCK_PASSWORD_CIPHERTEXT')}")
        print(f"Stored ENCRYPTION_KEY_ID: {creds.get('ENCRYPTION_KEY_ID')}")
        print(f"Decrypted password: {creds.get('M_STOCK_PASSWORD_DECRYPTED')}")

        # Optional round-trip check
        if plain_password:
            if creds.get("M_STOCK_PASSWORD_DECRYPTED") == plain_password:
                print("✅ Round-trip successful (matches original).")
            else:
                print("❌ Mismatch between original and decrypted password!")
        else:
            print("ℹ️ No plain password provided for comparison.")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    user_id = input("Enter M_STOCK_USER_ID to test: ").strip()
    plain_password = input("Enter original plain password (optional, press Enter to skip): ").strip() or None
    test_encryption(user_id, plain_password)