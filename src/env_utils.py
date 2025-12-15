import os

def update_env(user):
    """
    Update .env file with selected user's credentials.
    """
    env_path = os.path.join(os.getcwd(), "config", ".env")

    lines = [
        f"DB_HOST=localhost\n",
        f"DB_USER=root\n",
        f"DB_PASSWORD=root\n",
        f"DB_NAME=mstock\n",
        f"DB_PORT=3306\n",
        f"M_STOCK_USER_ID={user['M_STOCK_USER_ID']}\n",
        f"M_STOCK_PASSWORD={user['M_STOCK_PASSWORD']}\n",
        f"M_STOCK_API_KEY={user['M_STOCK_API_KEY']}\n",
        f"M_STOCK_API_KEY_TYPE={user['M_STOCK_API_KEY_TYPE']}\n"
    ]

    with open(env_path, "w") as f:
        f.writelines(lines)

    print(f".env updated for user {user['M_STOCK_USER_ID']}")