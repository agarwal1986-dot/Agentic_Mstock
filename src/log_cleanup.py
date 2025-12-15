from src import db

def cleanup_logs(days=30):
    """Delete logs older than N days (default: 30)"""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM logs
        WHERE TIMESTAMP < NOW() - INTERVAL %s DAY
    """, (days,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"[INFO] Logs older than {days} days have been deleted.")

if __name__ == "__main__":
    print("=== Log Cleanup Utility ===")
    days = input("Enter number of days to retain logs (default 30): ").strip()
    days = int(days) if days else 30

    print(f"\n[WARNING] This will permanently delete logs older than {days} days.")
    confirm = input("Type 'YES' to confirm cleanup, or anything else to cancel: ").strip().upper()

    if confirm == "YES":
        cleanup_logs(days)
    else:
        print("[INFO] Cleanup cancelled. No logs were deleted.")