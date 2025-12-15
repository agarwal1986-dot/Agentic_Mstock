# Agentic AI Workspace — Multi-Project Structure

A scalable, professional workspace for managing multiple AI/ML projects with shared Python 3.11.9 environment and reusable templates.

**Current Version**: 1.1 ✅ | **Status**: All critical issues resolved | **Last Updated**: Dec 12, 2025

## 📁 Complete Workspace Structure

```

C:\Agentic_Mstock\
│
├── src\
│   ├── __init__.py
│   ├── db.py                 # DB helpers

│       ├── __init__.py
│       ├── users.py          # Add / Update / Delete user
│
├── templates\
│   ├── __init__.py
│   ├── test_db_ops.py        # DB test script
├── Agentc_Env_01/                # Virtual environment (Python 3.11.9)
│
│
├── requirements/                 
├── docs/                         
│   └── README.md                 # Main project documentation (setup, usage, roadmap)
├── schema/                       
│   └── schema.sql                # MySQL schema (tables: tokens, holdings, orders, logs)
├── template/
│   ├── __init__.py
│   ├── test_db_ops.py        # DB test script
│   └── test_api_flow.py      # Full login/session flow
├── src/                          
│   ├── __init__.py               # Marks src as a Python package
├── src\
│   ├── __init__.py
│   └── api\
│       ├── __init__.py
│       ├── users.py          # Add / Update / Delete user
│       └── auth.py           # Login / OTP / Session
│   ├── holdings.py               # Functions to fetch and manage holdings data
│   ├── orders.py                 # Functions to place, modify, cancel orders
│   ├── market.py                 # Market data endpoints (quotes, charts, etc.)
│   ├── db.py                     # MySQL connection, CRUD operations for tokens/holdings/orders
│   └── utils.py                  # Shared utilities (logging, caching, banner messages)
│
├── src/tests/                    
│   ├── __init__.py               # Marks tests as a Python package
│   ├── test_auth.py              # Unit tests for auth.py (OTP verification, token caching)
│   ├── test_db.py                # Unit tests for db.py (DB connection, insert/retrieve tokens)
│   └── test_holdings.py          # Unit tests for holdings.py (portfolio fetch, data normalization)
│
└── streamlit_app/                
    └── app.py                    # Streamlit GUI scaffold (tabs for login, holdings, orders)

updateaed

AGENTIC_MSTOCK/
├── config/                  # Environment and DB config
│   ├── .env
│   └── db_config.json
├── schema/
│   └── schema.sql
├── src/                     # Core app code
│   ├── __init__.py
│   ├── db.py                # Updated DB connection module
│   ├── user_add.py
│   ├── user_update.py
│   ├── user_delete.py
│   ├── user_login.py
│   ├── auth.py
│   ├── env_utils.py
│   ├── users.py
│   └── tests/               # Test harness and connectivity checks
│       ├── __init__.py
│       ├── test_api_flow.py
│       ├── test_db_ops.py
│       └── test_mysql_connection.py
├── requirements/
│   ├── requirements-all.txt
│   ├── requirements-core.txt
│   ├── requirements-dev.txt
│   └── requirements-extended.txt
├── templates/               # Reserved for UI templates (if needed)
├── streamlit_app/           # Streamlit UI (future)
├── docs/
├── .gitignore
└── readme.md
```

## 🚀 Quick Start (30 seconds)


```
## ⚙️ Setup Instructions

### 1. Create and Activate Virtual Environment
```powershell
cd C:\Agentic_Mstock
python -m venv Agentc_Env_01
Agentc_Env_01\Scripts\activate

### 2. Upgrade Python

python -m pip install --upgrade pip


3. Install Dependencies
Navigate to the requirements folder and install all dependencies:
cd requirements
pip install -r requirements-all.txt


This installs:
- Core: requests, mysql-connector-python, python-dotenv, streamlit
- Dev: pytest, loguru, black
- Extended: LangChain ecosystem, ML/NLP libraries, pandas, scikit-learn, torch, transformers, SQLAlchemy, PyYAML, typer, click, rich, coloredlogs, opentelemetry, posthog
4. Verify Installation
Check installed packages:
pip list


Quick smoke test:
python -c "import requests, mysql.connector, streamlit, torch; print('✅ All imports working')"


5. Install MySQL Server (External)
- Download MySQL Community Edition from MySQL official site.
- Install MySQL Server + MySQL Workbench.
- Start the service (MySQL80) via Windows Services.
- Verify installation:
mysql --version

Suggested README Updates for MySQL
Add under Setup Instructions
### 5. Install MySQL Server (External)
- Download MySQL Community Edition from [MySQL official site](https://dev.mysql.com/downloads/).
- Install **MySQL Server** + **MySQL Workbench**.
- Start the service (`MySQL80`) via Windows Services.
- Verify installation:
  ```powershell
  mysql --version


6. Install MySQL Connector for Python
The project uses the official Oracle connector (mysql-connector-python).
pip install mysql-connector-python==9.0.0


Verify installation:
pip show mysql-connector-python


Expected output:
Name: mysql-connector-python
Version: 9.0.0


7. Smoke Test (Verify Imports)
Run a quick test to confirm all critical packages are working:
python -c "import requests, streamlit, torch; import mysql.connector; print('✅ All imports working')"


If you see ✅ All imports working, the environment is ready.

---
3. Database Setup
- Create database:
CREATE DATABASE mstock;
USE mstock;
- Apply schema:
SOURCE C:/Agentic_Mstock/schema/schema.sql;
- Tables created:
- tokens
- holdings
- orders
- logs

4. Configuration
- .env file (config/.env):
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=mstock



5. Testing Connection
Python Template
File: templates/test_mysql_connection.py
import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "mstock"),
        port=int(os.getenv("DB_PORT", 3306))
    )
    if conn.is_connected():
        print("✅ SUCCESS: MySQL connection established")
    else:
        print("❌ FAILURE: Connection attempt returned False")
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ ERROR: Connection failed\nDetails: {err}")


Run:
python templates/test_mysql_connection.py


Expected output:
✅ SUCCESS: MySQL connection established



6. Accessing MySQL
PowerShell (full path)
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p mstock


One‑liner test
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p mstock -e "SHOW TABLES;"


Workbench (GUI)
- Open MySQL Workbench → connect to Local instance MySQL80.
- Create DB if missing:
CREATE DATABASE mstock;
USE mstock;
- File → Open SQL Script → select schema.sql → Execute.
- Verify with:
SHOW TABLES;

- MStock API connection → this will handle authenticated requests for trading actions, account info, etc.
- WebSocket connection → this is essential for real‑time updates (market ticks, order status, live events). Instead of polling the API repeatedly, the WebSocket pushes updates automatically, which is far more efficient.
- Together → you’ll have a hybrid setup:
- API for on‑demand queries and actions (place order, fetch portfolio).
- WebSocket for continuous streaming data (live prices, trade confirmations).
So yes, testing both in Commit 02 makes sense. Once validated, we’ll merge it back into Commit 01 so your baseline includes a stable, real‑time trading foundation.

🟢 Next Steps (when you’re back)
- Test API connectivity → confirm authentication, basic GET/POST requests.
- Test WebSocket client → subscribe to a channel (e.g., live quotes) and verify streaming.
- Define integration points → how API + WebSocket data flow into your scripts (e.g., logging, vector DB later).

👉 When you return, do you want me to prepare a sandbox script outline for Commit 02 (mstock_connection_test.py) that includes both API and WebSocket test scaffolding, so you can plug in credentials and run immediately?


# Core dependencies
pip install -r requirements-core.txt

# Extended dependencies (includes TradingAPI A & B)
pip install -r requirements-extended.txt

# Or install everything
pip install -r requirements-all.txt

# Upgrade TradingAPI SDKs if needed *****
pip install --upgrade mStock-TradingApi-A
pip install --upgrade mStock-TradingApi-B

pip install -U pip setuptools

run gen_encription_key.py from requirements.

Table Design: S01_ENCRYPTION_KEY
Here’s a simple schema:
|  |  |  | 
| KEY_ID |  |  | 
| ENCRYPTION_KEY |  |  | 
| SYS_CREATION_DATE |  | CURRENT_TIMESTAMP | 

** ###########################TO DO  pasteevery thing above this  ** ###########################

add trotation for enccripton keys



