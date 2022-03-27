CREATE TABLE IF NOT EXISTS {TRADES_TABLE} (
    user_id VARCHAR(32) NOT NULL, 
    account VARCHAR(32) NOT NULL, 
    ticker VARCHAR(5) NOT NULL, 
    buy_date TEXT NOT NULL, 
    shares INTEGER NOT NULL, 
    buy_value REAL NOT NULL, 
    fees REAL NOT NULL, 
    sell_value REAL, 
    sell_date TEXT
);

CREATE TABLE IF NOT EXISTS {ACCOUNT_TYPES_TABLE} (
    name VARCHAR(16) NOT NULL PRIMARY KEY,
    information VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS {ACCOUNT_ATTRIBUTES_TABLE} (
    name VARCHAR(16) NOT NULL PRIMARY KEY,
    information VARCHAR(255),
    region VARCHAR(3)
);

CREATE TABLE IF NOT EXISTS {USERS_TABLE} (
    uuid VARCHAR(32) NOT NULL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    password BLOB NOT NULL,
    salt BLOB NOT NULL,
    latest_balance REAL
);

CREATE TABLE IF NOT EXISTS {ACCOUNTS_TABLE} (
    uuid VARCHAR(32) NOT NULL PRIMARY KEY,
    provider_id VARCHAR(32),
    owners VARCHAR(256) NOT NULL, /* Allow 8 different owners */
    name VARCHAR(64) NOT NULL,
    type_name VARCHAR(16) NOT NULL,
    attribute_name VARCHAR(16),
    latest_balance REAL,
    open_date TEXT,
    closed_date TEXT
);