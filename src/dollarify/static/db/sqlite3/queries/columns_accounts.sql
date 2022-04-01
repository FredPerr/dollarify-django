(
    uuid VARCHAR(32) NOT NULL PRIMARY KEY,
    provider_id VARCHAR(32),
    owners VARCHAR(256) NOT NULL,
    name VARCHAR(64) NOT NULL,
    type_name VARCHAR(16) NOT NULL,
    attribute_name VARCHAR(16),
    latest_balance REAL,
    open_date TEXT,
    closed_date TEXT
)