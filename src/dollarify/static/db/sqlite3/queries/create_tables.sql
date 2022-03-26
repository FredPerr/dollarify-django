CREATE TABLE IF NOT EXISTS {trade_table_name} (
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

CREATE TABLE IF NOT EXISTS {accounts_types_table_name} (
    name VARCHAR(16) NOT NULL PRIMARY KEY,
    information VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS {users_table_name} (
    uuid VARCHAR(32) NOT NULL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    password BLOB NOT NULL,
    salt BLOB NOT NULL,
    latest_balance REAL
);

CREATE TABLE IF NOT EXISTS {account_table_name} (
    uuid VARCHAR(32) NOT NULL PRIMARY KEY,
    provider_id VARCHAR(32),
    owners VARCHAR(256) NOT NULL, /* Allow 8 different owners */
    name VARCHAR(64) NOT NULL,
    type_name VARCHAR(16) NOT NULL,
    latest_balance REAL,
    open_date TEXT,
    closed_date TEXT
);