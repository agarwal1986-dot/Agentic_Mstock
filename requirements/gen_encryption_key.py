"""
Utility script to generate a Fernet encryption key and save it into:
1. SEC01_ENCRYPTION_KEY table (DB)
2. .env file in project root (ENCRYPTION_KEY and ENCRYPTION_KEY_ID)
"""

import os
import mysql.connector
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables from root .env
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(ROOT_DIR, ".env")
load_dotenv(env_path)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "mstock"),
        port=int(os.getenv("DB_PORT", 3306))
    )

def main():
    try:
        # Generate new Fernet key
        key = Fernet.generate_key().decode()

        # Insert into DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO SEC01_ENCRYPTION_KEY (ENCRYPTION_KEY) VALUES (%s)",
            (key,)
        )
        conn.commit()

        # Get the auto-incremented KEY_ID
        key_id = cursor.lastrowid

        cursor.close()
        conn.close()
        print(f"✅ ENCRYPTION_KEY inserted into SEC01_ENCRYPTION_KEY with KEY_ID={key_id}")

        # Update .env with both ENCRYPTION_KEY and ENCRYPTION_KEY_ID
        if not os.path.exists(env_path):
            with open(env_path, "w") as f:
                f.write("")

        with open(env_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        found_key = False
        found_id = False
        for line in lines:
            if line.startswith("ENCRYPTION_KEY="):
                new_lines.append(f"ENCRYPTION_KEY={key}\n")
                found_key = True
            elif line.startswith("ENCRYPTION_KEY_ID="):
                new_lines.append(f"ENCRYPTION_KEY_ID={key_id}\n")
                found_id = True
            else:
                new_lines.append(line)

        if not found_key:
            new_lines.append(f"ENCRYPTION_KEY={key}\n")
        if not found_id:
            new_lines.append(f"ENCRYPTION_KEY_ID={key_id}\n")

        with open(env_path, "w") as f:
            f.writelines(new_lines)

        print(f"✅ ENCRYPTION_KEY and ENCRYPTION_KEY_ID written to {env_path}")
        print(f"🔑 Key value: {key}")
        print(f"🆔 Key ID: {key_id}")
        print("⚠️ Keep this key safe! Do not commit it to version control.")

    except Exception as e:
        print("❌ Failed to generate or save ENCRYPTION_KEY:", str(e))

if __name__ == "__main__":
    main()