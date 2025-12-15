-- schema.sql — Database schema for MStock project

-- Create database (run once)
CREATE DATABASE IF NOT EXISTS mstock;
USE mstock;

-- -------------------------------
-- Tokens Table
-- -------------------------------
-- Reset schema: drop old tables if they exist
DROP TABLE IF EXISTS tokens;
DROP TABLE IF EXISTS holdings;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS logs;

-- Create refined authentication credential table
CREATE TABLE MS01_API_Authentication_Credential (
    CUST_SEQ_ID             INT AUTO_INCREMENT PRIMARY KEY,   -- Unique identifier
    SYS_CREATE_DATE_TIME    TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Record creation time
    SYS_UPDATE_DATE_TIME    TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                            ON UPDATE CURRENT_TIMESTAMP,       -- Record update time
    
    M_STOCK_USER_ID         VARCHAR(100) NOT NULL,            -- Username
    M_STOCK_PASSWORD        VARCHAR(255) NOT NULL,            -- Password (to be encrypted later)
    M_STOCK_API_KEY         VARCHAR(255) NOT NULL,            -- API Key (to be encrypted later)
    M_STOCK_API_KEY_TYPE    ENUM('A','B') NOT NULL,           -- API Key type
    M_CLIENT_CODE VARCHAR(50),
    M_RESPONSE_USER_ID VARCHAR(50),
    M_RESPONSE_USER_NAME VARCHAR(100),
    M_ACCESS_TOKEN TEXT,
    M_PUBLIC_TOKEN TEXT,
    M_REFRESH_TOKEN TEXT,
    M_ENC_TOKEN TEXT,
    LAST_LOGIN_DATE TIMESTAMP,
    LAST_LOGOUT_DATE TIMESTAMP,
    ENCRYPTION_KEY_ID TEXT
);
-- -------------------------------
-- Logs Table
-- -------------------------------

DROP TABLE IF EXISTS logs;

CREATE TABLE logs (
    LOG_ID              INT AUTO_INCREMENT PRIMARY KEY,
    SYS_CREATE_DATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    SYS_UPDATE_DATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    LOG_LEVEL           ENUM('INFO','WARN','ERROR') NOT NULL,
    LOG_MESSAGE         TEXT NOT NULL,
    SOURCE_MODULE       VARCHAR(100) NULL
);

CREATE TABLE MS01_REQUEST_RESPONSE_LOG (
    id INT PRIMARY KEY AUTO_INCREMENT,
    log_level VARCHAR(20) NOT NULL,         -- e.g. INFO, ERROR
    message VARCHAR(255) NOT NULL,          -- short description
    module VARCHAR(100) NOT NULL,           -- e.g. 'mstock_auth_api_cli'
    request TEXT,                           -- request payload (JSON/string)
    response TEXT,                          -- response payload (JSON/string)
    api_name VARCHAR(100),
    SYS_CREATE_DATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    LOGIN_SEQ_ID VARCHAR(20)
);


 -- Saving encription Key 

CREATE TABLE SEC01_ENCRYPTION_KEY (
    KEY_ID INT AUTO_INCREMENT PRIMARY KEY,
    ENCRYPTION_KEY VARCHAR(255) NOT NULL,
    SYS_CREATE_DATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

