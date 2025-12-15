from src import db

# Insert dummy credential
db.insert_credential("demo_user", "demo_pass", "demo_api_key", "A")

# Fetch latest credential
cred = db.get_latest_credential()
print("Latest Credential:", cred)

# Insert log
db.insert_log("INFO", "Inserted demo credential", "test_db_ops")