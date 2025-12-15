"""
Template: test_mysql_connection.py
Quick script to validate MySQL connection using .env credentials.
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "mstock"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        if conn.is_connected():
            print("\n==============================")
            print("✅ SUCCESS: MySQL connection established")
            print("==============================\n")
        else:
            print("\n==============================")
            print("❌ FAILURE: Connection attempt returned False")
            print("==============================\n")
        conn.close()
    except mysql.connector.Error as err:
        print("\n==============================")
        print("❌ ERROR: Connection failed")
        print(f"Details: {err}")
        print("==============================\n")

if __name__ == "__main__":
    test_connection()