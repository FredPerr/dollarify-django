(
    uuid VARCHAR(32) NOT NULL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    password BLOB NOT NULL,
    salt BLOB NOT NULL,
    latest_balance REAL
)