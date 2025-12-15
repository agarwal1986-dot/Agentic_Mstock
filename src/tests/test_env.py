import os
import sys
import importlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Step 1: Check DB environment variables ---
print("🔍 Checking environment variables...")
required_env_vars = [
    "DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"❌ Missing environment variables: {missing_vars}")
else:
    print("✅ All required DB environment variables are set.")

# --- Step 2: Check TradingAPI environment placeholders ---
trading_env_vars = [
    "M_STOCK_USER_ID", "M_STOCK_PASSWORD", "M_STOCK_API_KEY", "M_STOCK_API_KEY_TYPE"
]

missing_trading = [var for var in trading_env_vars if not os.getenv(var)]
if missing_trading:
    print(f"⚠️ TradingAPI variables missing or set to placeholders: {missing_trading}")
else:
    print("✅ TradingAPI environment variables are set.")

# --- Step 3: Check dependencies ---
print("\n🔍 Checking Python dependencies...")
dependencies = [
    "mysql.connector",   # MySQL driver
    "dotenv",            # python-dotenv
    "requests",          # HTTP client
    "streamlit",         # optional GUI
    "tradingapi_a.mconnect",  # Type A SDK
    "tradingapi_b.mconnect"   # Type B SDK
]

for dep in dependencies:
    try:
        importlib.import_module(dep)
        print(f"✅ {dep} is installed.")
    except ImportError:
        print(f"❌ {dep} is NOT installed.")

# --- Step 4: Final summary ---
print("\n🎯 Environment test completed.")