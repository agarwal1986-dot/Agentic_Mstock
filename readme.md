# Agentic AI Workspace — Multi-Project Structure

A scalable, professional workspace for managing multiple AI/ML projects with shared Python 3.11.9 environment and reusable templates. Currently focused on mStock Trading API authentication and user management system.

**Current Version**: 2.0 ✅ | **Status**: Core Features Implemented | **Last Updated**: December 2024

---

## 📋 Table of Contents
 [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Database Schema](#database-schema)
- [Security](#security)
- [Maintenance](#maintenance)
- [Future Plans](#future-plans)
- [TODO](#todo)
- [Dependencies](#dependencies)
-

## 🎯 Overview

This project provides a secure foundation for managing mStock Trading API authentication. It handles user credential management, encrypted password storage, login/logout flows, and comprehensive request/response logging.

**Key Capabilities:**
- ✅ Secure credential storage with Fernet encryption
- ✅ User management (Add, Update, Delete)
- ✅ mStock API authentication flow (Login/Logout)
- ✅ Request/response logging with unique sequence IDs
- ✅ Database persistence with MySQL
- ✅ Environment variable management
- ✅ CLI tools for operations

---

## ✨ Features

### Implemented Features

1. **User Management**
   - Add new users with encrypted passwords
   - Update user credentials (password, API key, API key type)
   - Delete users
   - Support for multiple API key types (Type A/B)

2. **Authentication System**
   - Login flow with mStock API integration
   - OTP/Request token handling
   - Session token generation
   - Logout functionality
   - Token persistence in database

3. **Security**
   - Password encryption using Fernet (symmetric encryption)
   - Encryption key rotation support
   - Key versioning with `ENCRYPTION_KEY_ID`
   - Secure credential retrieval with automatic decryption

4. **Logging & Monitoring**
   - Simple log entries (INFO, WARN, ERROR)
   - Detailed request/response logging
   - Unique login sequence IDs for tracking flows
   - Log cleanup utility

5. **Database Operations**
   - MySQL connection management
   - CRUD operations for credentials
   - Transaction support
   - Error handling and recovery

6. **CLI Tools**
   - Interactive user management menu
   - Login/logout CLI commands
   - Test scripts for validation

---

## 📁 Project Structure

```
Agentic_Mstock/
├── config/                  # Environment and DB config
│   └── db_config.json
├── schema/
│   └── schema.sql           # MySQL database schema
├── src/                     # Core app code
│   ├── __init__.py
│   ├── api/                 # API module (reserved for future use)
│   │   └── __init__.py
│   ├── db.py                # Database connection & CRUD operations
│   ├── auth.py              # mStock API authentication functions
│   ├── users.py             # User management functions
│   ├── config.py            # Encryption/decryption utilities
│   ├── env_utils.py         # Environment variable helpers
│   ├── log_cleanup.py       # Log cleanup utility
│   ├── mstock_auth_api_cli.py  # Main CLI for login/logout
│   ├── user_add.py          # CLI: Add user
│   ├── user_update.py       # CLI: Update user
│   ├── user_delete.py       # CLI: Delete user
│   ├── user_login.py        # CLI: Login user
│   └── tests/               # Test harness and connectivity checks
│       ├── __init__.py
│       ├── test_api_flow.py
│       ├── test_db_ops.py
│       ├── test_decryption.py
│       ├── test_mysql_connection.py
│       ├── test_env.py
│       ├── test_env_dependencies.py
│       └── db_queries.txt
├── requirements/
│   ├── requirements-all.txt
│   ├── requirements-core.txt
│   ├── requirements-dev.txt
│   ├── requirements-extended.txt
│   └── gen_encryption_key.py  # Generate encryption key utility
├── templates/               # Reserved for UI templates (if needed)
├── streamlit_app/           # Streamlit UI (future)
├── docs/                         
│   └── README.md                 # Main project documentation (setup, usage, roadmap)
│   └── __init__.py
├── config.py                # Root-level config (encryption utilities)
├── .gitignore
└── readme.md
```

**Note**: The `.env` file should be created in the `config/` directory during setup (not tracked in git).

---

## 🔧 Prerequisites

### Required Software

1. **Python 3.11.9+**
   ```powershell
   python --version
   ```

2. **Git** (for version control)

### System Requirements

- **OS**: Windows 10/11 (tested), Linux/macOS (should work)
- **RAM**: 4GB minimum
- **Disk**: 500MB free space

---

## 🚀 Installation

### Step 1: Install MySQL Server

**⚠️ IMPORTANT: MySQL Server must be installed and running before proceeding with database setup.**

1. **Download MySQL Server**
   - Download MySQL Community Edition from [MySQL Official Site](https://dev.mysql.com/downloads/)
   - Install MySQL Server + MySQL Workbench

2. **Start MySQL Service**
   ```powershell
   # Check if MySQL service is running
   Get-Service MySQL80
   
   # If not running, start it
   Start-Service MySQL80
   ```

3. **Verify Installation**
   ```powershell
   mysql --version
   ```

4. **Set Root Password** (if not done during installation)
   ```powershell
   # Access MySQL as root
   mysql -u root -p
   ```

**Note**: Remember your MySQL root password - you'll need it for database configuration.

### Step 2: Clone Repository

```powershell
cd C:\cursor_learning\Agentic_Mstock
git clone <repository-url> Agentic_Mstock
cd Agentic_Mstock
```

### Step 3: Create Virtual Environment

```powershell
cd C:\Agentic_Mstock
python -m venv Agentc_Env_01
Agentc_Env_01\Scripts\activate
```

### Step 4: Upgrade pip and setuptools

```powershell
python -m pip install --upgrade pip setuptools
```

### Step 5: Install Dependencies

**Option A: Install Core Dependencies Only** (Recommended for basic usage)
```powershell
cd requirements
pip install -r requirements-core.txt
```

**Option B: Install Extended Dependencies** (Includes TradingAPI A & B and ML/AI libraries)
```powershell
pip install -r requirements-extended.txt
```

**Option C: Install All Dependencies** (Includes everything)
```powershell
pip install -r requirements-all.txt
```

**What gets installed:**
- **Core**: `requests`, `mysql-connector-python`, `python-dotenv`, `streamlit`
- **Dev**: `pytest`, `loguru`, `black`
- **Extended**: LangChain ecosystem, ML/NLP libraries, pandas, scikit-learn, torch, transformers, SQLAlchemy, PyYAML, typer, click, rich, coloredlogs, opentelemetry, posthog
- **TradingAPI**: `mStock-TradingApi-A`, `mStock-TradingApi-B`

### Step 6: Upgrade TradingAPI SDKs (Optional)

If you need the latest versions of TradingAPI SDKs:

```powershell
pip install --upgrade mStock-TradingApi-A
pip install --upgrade mStock-TradingApi-B
```

### Step 7: Verify Installation

```powershell
# Check installed packages
pip list

# Quick smoke test
python -c "import requests, mysql.connector, dotenv; print('✅ Core packages installed')"
```

Expected output:
```
✅ Core packages installed
```

### Step 8: Setup MySQL Database

**⚠️ Prerequisite: MySQL Server must be installed and running (Step 1)**

1. **Start MySQL Service** (if not already running)
   ```powershell
   Get-Service MySQL80
   ```

2. **Create Database**
   ```sql
   CREATE DATABASE mstock;
   USE mstock;
   ```
   
   Or via command line:
   ```powershell
   mysql -u root -p -e "CREATE DATABASE mstock;"
   ```

3. **Apply Schema**
   ```powershell
   # Using MySQL command line
   mysql -u root -p mstock < schema\schema.sql
   
   # Or using MySQL Workbench:
   # File → Open SQL Script → Select schema/schema.sql → Execute
   ```

4. **Verify Tables**
   ```sql
   USE mstock;
   SHOW TABLES;
   -- Should show:
   -- MS01_API_Authentication_Credential
   -- logs
   -- MS01_REQUEST_RESPONSE_LOG
   -- SEC01_ENCRYPTION_KEY
   ```
   
   Or via command line:
   ```powershell
   mysql -u root -p mstock -e "SHOW TABLES;"
   ```

### Step 9: Generate Encryption Key

```powershell
# Ensure you're in the project root
python requirements\gen_encryption_key.py
```

This will:
- Generate a Fernet encryption key
- Store it in `SEC01_ENCRYPTION_KEY` table
- Update `.env` file with `ENCRYPTION_KEY` and `ENCRYPTION_KEY_ID`

**Note**: This step requires the database to be set up (Step 8).

### Step 10: Configure Environment Variables

Create `config/.env` file:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=mstock
DB_PORT=3306

# Encryption (auto-generated by gen_encryption_key.py)
ENCRYPTION_KEY=your_generated_key_here
ENCRYPTION_KEY_ID=1

# mStock API Credentials (set when adding users)
M_STOCK_USER_ID=
M_STOCK_PASSWORD=
M_STOCK_API_KEY=
M_STOCK_API_KEY_TYPE=A
```

**⚠️ Security Note**: Never commit `.env` file to version control. It's already in `.gitignore`.

### Step 11: Test Database Connection

```powershell
python src\tests\test_mysql_connection.py
```

Expected output:
```
✅ SUCCESS: MySQL connection established
```

---

## ⚙️ Configuration

### Database Configuration

Edit `config/db_config.json` or set environment variables in `.env`:

```json
{
  "host": "localhost",
  "user": "root",
  "password": "yourpassword",
  "database": "mstock"
}
```

### mStock API Configuration

- **API Base URL**: `https://api.mstock.trade/openapi/typea` (Type A)
- **API Key Types**: `A` or `B`
- **Authentication Flow**: Login → OTP → Session Token

---

## 📖 Usage

### User Management

#### Add a New User

```powershell
python src\user_add.py
```

Interactive prompts:
- M_STOCK_USER_ID
- M_STOCK_PASSWORD (masked input)
- M_STOCK_API_KEY
- M_STOCK_API_KEY_TYPE (A/B)

#### Update User

```powershell
python src\user_update.py
```

#### Delete User

```powershell
python src\user_delete.py
```

#### Interactive User Management Menu

```powershell
python src\tests\test_api_flow.py
```

Menu options:
1. Add User
2. Update User
3. Delete User
4. Run All (Add → Update → Delete)
5. Exit
6. View Logs

### Authentication

#### Login

```powershell
python src\mstock_auth_api_cli.py login
```

Flow:
1. Enter mStock User ID
2. System fetches credentials from DB
3. Sends login request to mStock API
4. Enter 3-digit OTP (request token)
5. Generates session token
6. Updates database with tokens
7. Updates `.env` file

#### Logout

```powershell
python src\mstock_auth_api_cli.py logout
```

### Testing

#### Test Database Connection

```powershell
python src\tests\test_mysql_connection.py
```

#### Test Encryption/Decryption

```powershell
python src\tests\test_decryption.py
```

#### Test Database Operations

```powershell
python src\tests\test_db_ops.py
```

### Utilities

#### Cleanup Old Logs

```powershell
python src\log_cleanup.py
```

---

## 🗄️ Database Schema

### Overview

The database consists of four main tables that handle authentication credentials, encryption keys, and logging functionality.

### Table: MS01_API_Authentication_Credential

Stores user credentials, API keys, and authentication tokens for mStock Trading API.

| Column Name | Data Type | Constraints | Default | Description |
|------------|-----------|-------------|---------|-------------|
| `CUST_SEQ_ID` | INT | PRIMARY KEY, AUTO_INCREMENT | - | Unique identifier for each credential record |
| `SYS_CREATE_DATE_TIME` | TIMESTAMP | - | CURRENT_TIMESTAMP | Record creation timestamp |
| `SYS_UPDATE_DATE_TIME` | TIMESTAMP | - | CURRENT_TIMESTAMP ON UPDATE | Record last update timestamp |
| `M_STOCK_USER_ID` | VARCHAR(100) | NOT NULL | - | mStock username/user ID |
| `M_STOCK_PASSWORD` | VARCHAR(255) | NOT NULL | - | Encrypted password (Fernet encryption) |
| `M_STOCK_API_KEY` | VARCHAR(255) | NOT NULL | - | mStock API key |
| `M_STOCK_API_KEY_TYPE` | ENUM('A','B') | NOT NULL | - | API key type (A or B) |
| `M_CLIENT_CODE` | VARCHAR(50) | NULL | - | Client code from API response |
| `M_RESPONSE_USER_ID` | VARCHAR(50) | NULL | - | User ID from API response |
| `M_RESPONSE_USER_NAME` | VARCHAR(100) | NULL | - | User name from API response |
| `M_ACCESS_TOKEN` | TEXT | NULL | - | Access token for API authentication |
| `M_PUBLIC_TOKEN` | TEXT | NULL | - | Public token from API |
| `M_REFRESH_TOKEN` | TEXT | NULL | - | Refresh token for token renewal |
| `M_ENC_TOKEN` | TEXT | NULL | - | Encrypted token from API |
| `LAST_LOGIN_DATE` | TIMESTAMP | NULL | - | Last successful login timestamp |
| `LAST_LOGOUT_DATE` | TIMESTAMP | NULL | - | Last logout timestamp |
| `ENCRYPTION_KEY_ID` | TEXT | NULL | - | Reference to encryption key version used |

### Table: SEC01_ENCRYPTION_KEY

Stores encryption keys with versioning support for password encryption/decryption.

| Column Name | Data Type | Constraints | Default | Description |
|------------|-----------|-------------|---------|-------------|
| `KEY_ID` | INT | PRIMARY KEY, AUTO_INCREMENT | - | Unique identifier for encryption key version |
| `ENCRYPTION_KEY` | VARCHAR(255) | NOT NULL | - | Fernet encryption key (base64 encoded) |
| `SYS_CREATE_DATE_TIME` | TIMESTAMP | - | CURRENT_TIMESTAMP | Key creation timestamp |

### Table: logs

Stores simple log entries for application events and errors.

| Column Name | Data Type | Constraints | Default | Description |
|------------|-----------|-------------|---------|-------------|
| `LOG_ID` | INT | PRIMARY KEY, AUTO_INCREMENT | - | Unique identifier for log entry |
| `SYS_CREATE_DATE_TIME` | TIMESTAMP | - | CURRENT_TIMESTAMP | Log entry creation timestamp |
| `SYS_UPDATE_DATE_TIME` | TIMESTAMP | - | CURRENT_TIMESTAMP ON UPDATE | Log entry last update timestamp |
| `LOG_LEVEL` | ENUM('INFO','WARN','ERROR') | NOT NULL | - | Log severity level |
| `LOG_MESSAGE` | TEXT | NOT NULL | - | Log message content |
| `SOURCE_MODULE` | VARCHAR(100) | NULL | - | Source module/component that generated the log |

### Table: MS01_REQUEST_RESPONSE_LOG

Stores detailed request/response logs for API calls with unique sequence tracking.

| Column Name | Data Type | Constraints | Default | Description |
|------------|-----------|-------------|---------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | - | Unique identifier for log entry |
| `log_level` | VARCHAR(20) | NOT NULL | - | Log severity level (e.g., INFO, ERROR) |
| `message` | VARCHAR(255) | NOT NULL | - | Short description of the log entry |
| `module` | VARCHAR(100) | NOT NULL | - | Source module name (e.g., 'mstock_auth_api_cli') |
| `request` | TEXT | NULL | - | Request payload (JSON/string format) |
| `response` | TEXT | NULL | - | Response payload (JSON/string format) |
| `api_name` | VARCHAR(100) | NULL | - | API endpoint name (e.g., 'login', 'generate_session') |
| `SYS_CREATE_DATE_TIME` | TIMESTAMP | - | CURRENT_TIMESTAMP | Log entry creation timestamp |
| `LOGIN_SEQ_ID` | VARCHAR(20) | NULL | - | Unique sequence ID for tracking login flows |

### Key Relationships

- `MS01_API_Authentication_Credential.ENCRYPTION_KEY_ID` → `SEC01_ENCRYPTION_KEY.KEY_ID`
  - Links user credentials to the encryption key version used for password encryption

### Important Notes

- **Password Encryption**: `M_STOCK_PASSWORD` is stored encrypted using Fernet encryption. The `ENCRYPTION_KEY_ID` field tracks which encryption key version was used.
- **Token Storage**: Authentication tokens (`M_ACCESS_TOKEN`, `M_REFRESH_TOKEN`, `M_ENC_TOKEN`) are stored in plain text as they are already encrypted by the mStock API.
- **Logging**: Two separate logging tables exist:
  - `logs`: Simple application logs
  - `MS01_REQUEST_RESPONSE_LOG`: Detailed API request/response logs with sequence tracking
- **Sequence Tracking**: `LOGIN_SEQ_ID` in `MS01_REQUEST_RESPONSE_LOG` allows tracking of complete login flows across multiple API calls.

---

## 🔒 Security

### Encryption

- **Algorithm**: Fernet (symmetric encryption)
- **Key Management**: Database-stored with versioning
- **Key Rotation**: Supported via `ENCRYPTION_KEY_ID`
- **Password Storage**: Always encrypted at rest

### Best Practices

1. ✅ Never commit `.env` files
2. ✅ Use strong encryption keys
3. ✅ Rotate encryption keys periodically (see TODO section)
4. ✅ Use masked password input (`getpass`)
5. ✅ Log security events
6. ✅ Validate user inputs

### Security Features

- Password encryption before database storage
- Automatic decryption on retrieval
- Support for multiple encryption key versions
- Secure credential handling in memory

---

## 🔧 Maintenance

This section will be updated with maintenance procedures, schedules, and best practices.

### Regular Maintenance Tasks

_To be updated_

### Maintenance Schedule

_To be updated_

### Maintenance Procedures

_To be updated_

---

## 🧪 Testing

### Test Coverage

- ✅ Database connection tests
- ✅ Encryption/decryption tests
- ✅ User CRUD operations
- ✅ API flow tests
- ✅ Environment validation

### Running Tests

```powershell
# Run all tests
pytest src/tests/

# Run specific test
pytest src/tests/test_db_ops.py -v
```

---

## 🔮 Future Plans

### Phase 1: Trading Operations (Planned)
- [ ] Holdings management (fetch portfolio)
- [ ] Order placement (buy/sell)
- [ ] Order modification and cancellation
- [ ] Order history tracking

### Phase 2: Market Data (Planned)
- [ ] Real-time quotes
- [ ] Historical data
- [ ] Chart data endpoints
- [ ] Market depth

### Phase 3: Real-time Updates (Planned)
- [ ] WebSocket integration
- [ ] Live market tick updates
- [ ] Order status notifications
- [ ] Portfolio updates

### Phase 4: User Interface (Planned)
- [ ] Streamlit web application
- [ ] Dashboard for portfolio view
- [ ] Trading interface
- [ ] Analytics and reporting

### Phase 5: Advanced Features (Planned)
- [ ] Agentic AI integration (LangChain)
- [ ] Automated trading strategies
- [ ] Risk management
- [ ] Backtesting framework
- [ ] Vector database for trade analysis

---

## 📝 TODO

### High Priority

#### Schema Definition for Future Code
- [ ] Define schema for `holdings` table
  - [ ] Portfolio positions structure
  - [ ] Symbol, quantity, average price, current value
  - [ ] Last updated timestamp
  - [ ] Foreign key relationship to user credentials
- [ ] Define schema for `orders` table
  - [ ] Order ID, symbol, quantity, price
  - [ ] Order type (market/limit), side (buy/sell)
  - [ ] Order status (pending/filled/cancelled/rejected)
  - [ ] Timestamps (created, executed, cancelled)
  - [ ] Foreign key relationship to user credentials
- [ ] Define schema for `market_data` table (if needed)
  - [ ] Symbol, price, volume, timestamp
  - [ ] Historical data storage structure
  - [ ] Indexes for performance
- [ ] Define schema for `trading_strategies` table (future)
  - [ ] Strategy name, parameters, status
  - [ ] Performance metrics
  - [ ] Backtest results
- [ ] Define schema for `portfolio_history` table
  - [ ] Snapshot of portfolio at different timestamps
  - [ ] Historical performance tracking
- [ ] Create migration scripts for schema updates
- [ ] Document schema relationships and foreign keys
- [ ] Add indexes for frequently queried fields
- [ ] Define constraints and validation rules

#### Error Handling
- [ ] Implement comprehensive try-catch blocks in all API calls
- [ ] Add retry logic for transient failures
  - [ ] Exponential backoff strategy
  - [ ] Maximum retry attempts configuration
  - [ ] Retry for specific HTTP status codes
- [ ] Create custom exception classes
  - [ ] `DatabaseConnectionError`
  - [ ] `EncryptionError`
  - [ ] `AuthenticationError`
  - [ ] `APIError`
  - [ ] `ValidationError`
  - [ ] `ConfigurationError`
- [ ] Add error logging with context
  - [ ] Stack traces for debugging
  - [ ] User-friendly error messages
  - [ ] Error categorization
- [ ] Implement graceful degradation for non-critical failures
- [ ] Add user-friendly error messages for end users
- [ ] Create error recovery mechanisms
  - [ ] Automatic retry for failed operations
  - [ ] Fallback to cached data when available
- [ ] Add validation for all user inputs
  - [ ] Input sanitization
  - [ ] Type checking
  - [ ] Range validation
- [ ] Implement timeout handling for API requests
  - [ ] Configurable timeout values
  - [ ] Timeout error handling
- [ ] Add circuit breaker pattern for external API calls
  - [ ] Prevent cascading failures
  - [ ] Automatic recovery after cooldown period
- [ ] Create error monitoring and alerting
  - [ ] Error rate tracking
  - [ ] Critical error notifications

#### GUI Creation
- [ ] Design Streamlit application structure
  - [ ] Login/authentication page
  - [ ] Dashboard/home page
  - [ ] User management interface
  - [ ] Portfolio/holdings view
  - [ ] Order placement interface
  - [ ] Order history view
  - [ ] Settings/configuration page
  - [ ] Analytics and reporting page
- [ ] Implement user authentication UI
  - [ ] Login form with validation
  - [ ] Session management
  - [ ] Logout functionality
- [ ] Create user management forms (add/edit/delete)
  - [ ] Add user form with validation
  - [ ] Edit user form with pre-filled data
  - [ ] Delete user with confirmation
  - [ ] User list with search/filter
- [ ] Build portfolio visualization dashboard
  - [ ] Holdings table with real-time data
  - [ ] Portfolio value charts
  - [ ] Asset allocation pie chart
  - [ ] Performance metrics display
- [ ] Design order placement forms
  - [ ] Buy/sell order form
  - [ ] Market/limit order selection
  - [ ] Order preview and confirmation
  - [ ] Order status tracking
- [ ] Add real-time data display components
  - [ ] Live price updates
  - [ ] Order status updates
  - [ ] Portfolio value updates
- [ ] Implement responsive design for mobile/tablet
  - [ ] Mobile-friendly layouts
  - [ ] Touch-friendly controls
- [ ] Add dark/light theme support
  - [ ] Theme toggle
  - [ ] Persistent theme preference
- [ ] Create navigation menu and routing
  - [ ] Sidebar navigation
  - [ ] Page routing logic
  - [ ] Active page highlighting
- [ ] Add data tables with sorting/filtering
  - [ ] Sortable columns
  - [ ] Search functionality
  - [ ] Pagination
- [ ] Implement charts and graphs for analytics
  - [ ] Portfolio performance line chart
  - [ ] Asset allocation pie chart
  - [ ] Trade history bar chart
- [ ] Add export functionality (CSV/PDF)
  - [ ] Export holdings to CSV
  - [ ] Export order history
  - [ ] Generate PDF reports
- [ ] Create help/documentation section
  - [ ] User guide
  - [ ] FAQ section
  - [ ] API documentation link

#### Encryption Key Rotation (To Be Done)
- [ ] Create automated key rotation script (`src/maintenance/rotate_encryption_keys.py`)
  - [ ] Generate new encryption key
  - [ ] Re-encrypt all existing credentials with new key
  - [ ] Update `ENCRYPTION_KEY_ID` for all users
  - [ ] Archive old keys for backward compatibility
  - [ ] Verify all credentials are accessible after rotation
- [ ] Implement key expiration dates
  - [ ] Add expiration date field to `SEC01_ENCRYPTION_KEY` table
  - [ ] Create alert system for keys nearing expiration
  - [ ] Automatic rotation trigger based on expiration
- [ ] Add automatic re-encryption of all credentials
  - [ ] Batch processing for large user bases
  - [ ] Progress tracking and reporting
  - [ ] Rollback capability if errors occur
- [ ] Implement key rotation audit logging
  - [ ] Log all key rotation events
  - [ ] Track who performed rotation and when
  - [ ] Document reason for rotation
- [ ] Add rollback capability
  - [ ] Ability to revert to previous key
  - [ ] Restore credentials encrypted with old key
  - [ ] Safety checks before rollback
- [ ] Create scheduled rotation reminders
  - [ ] Email/notification system for rotation due dates
  - [ ] Dashboard showing key age and rotation status
  - [ ] Integration with calendar for maintenance windows

### Medium Priority
- [ ] Implement encryption key rotation mechanism (see TODO section above)
- [ ] Add comprehensive error handling for API failures
- [ ] Implement token refresh logic
- [ ] Add input validation for all user inputs
- [ ] Create API documentation (OpenAPI/Swagger)
- [ ] Add unit tests for all modules
- [ ] Implement logging configuration file
- [ ] Add database migration scripts
- [ ] Create deployment documentation
- [ ] Add performance monitoring

### Low Priority
- [ ] Add support for multiple database backends
- [ ] Implement caching layer
- [ ] Add rate limiting for API calls
- [ ] Create Docker containerization
- [ ] Add CI/CD pipeline

### Known Issues
- [ ] `config.py` has dummy login/logout functions (needs real API integration)
- [ ] Some test files reference old module paths
- [ ] Log cleanup utility needs confirmation prompt improvement

---

## 📚 Dependencies

### Core Dependencies
- `requests>=2.32.5` - HTTP client for API calls
- `mysql-connector-python==9.0.0` - MySQL database driver
- `python-dotenv==1.2.1` - Environment variable management
- `cryptography` - Encryption/decryption (Fernet)
- `streamlit==1.40.0` - Web app framework (for future GUI)

### Development Dependencies
- `pytest==8.3.5` - Testing framework
- `loguru==0.7.2` - Advanced logging
- `black==24.10.0` - Code formatter

### Extended Dependencies (Optional)
- `mStock-TradingApi-A` - mStock Trading API SDK (Type A)
- `mStock-TradingApi-B==1.0.5` - mStock Trading API SDK (Type B)
- `langchain==1.1.0` - AI/Agent framework
- `pandas==2.3.3`, `numpy==1.26.4` - Data processing
- `torch==2.9.1`, `transformers==4.46.3` - ML/NLP libraries
- `fastapi==0.115.0` - API framework
- `chromadb==0.5.23` - Vector database

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

[Specify your license here]

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: [Your contact information]

---

## 🎯 Quick Start Checklist

- [ ] Python 3.11.9+ installed
- [ ] MySQL Server installed and running
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Database created and schema applied
- [ ] Encryption key generated
- [ ] `.env` file configured
- [ ] Test database connection
- [ ] Add a test user
- [ ] Test login flow

---

**Last Updated**: December 2024  
**Maintained By**: [Your Name/Team]
```

This README includes:
- ✅ Project structure with annotations/comments preserved
- ✅ Proper tree formatting with `├──`, `│`, and `└──`
- ✅ All sections organized and complete
- ✅ Installation steps in correct sequence
- ✅ Database schema in tabular format
- ✅ Clean formatting throughout

Ready to use.



