CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(100) NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(16),
    password VARCHAR(256) NOT NULL,
    salt VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS account_types (
    id SERIAL PRIMARY KEY,
    short_name VARCHAR(32),
    full_name VARCHAR(128) NOT NULL,
    information TEXT
);

CREATE TABLE IF NOT EXISTS account_attributes (
    id SERIAL PRIMARY KEY,
    short_name VARCHAR(32),
    full_name VARCHAR(128) NOT NULL,
    information TEXT
);

CREATE TABLE IF NOT EXISTS entities (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(32),
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS accounts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    account_type_id INTEGER NOT NULL,
    provider_id UUID NOT NULL,

    CONSTRAINT fk_type FOREIGN KEY(account_type_id) REFERENCES account_types(id) ON DELETE RESTRICT,
    CONSTRAINT fk_provider FOREIGN KEY(provider_id) REFERENCES entities(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS stock_markets (
    short_name VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(40) NOT NULL,
    timezone VARCHAR(12) NOT NULL,
    open_hour DECIMAL(3,2) NOT NULL,
    close_hour FLOAT NOT NULL,
    lunch_break_from DECIMAL(3,2),
    lunch_break_to DECIMAL(3,2),
    holidays VARCHAR(50)[]
);

CREATE TABLE IF NOT EXISTS stock_market_trades (
    id SERIAL PRIMARY KEY,
    account_type_id INTEGER NOT NULL,
    stock_market VARCHAR(10),
    ticker VARCHAR(8) NOT NULL,
    bought_at MONEY NOT NULL,
    shares INTEGER NOT NULL,   
    bought_on TIMESTAMP DEFAULT (now()) NOT NULL,
    sold_on TIMESTAMP,

    CONSTRAINT stock_market_fk FOREIGN KEY(stock_market) REFERENCES stock_markets(short_name) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    provider_id UUID NOT NULL,
    amount MONEY NOT NULL,
    interest_rate DECIMAL(4,2) NOT NULL DEFAULT 0,
    due_date DATE,

    CONSTRAINT fk_provider FOREIGN KEY(provider_id) REFERENCES entities(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS transfers (
    id SERIAL PRIMARY KEY,
    source_account_id UUID NOT NULL,
    destination_account_id UUID NOT NULL,
    amount MONEY NOT NULL,
    datetime TIMESTAMP DEFAULT (now()) NOT NULL,

    CONSTRAINT fk_source_account FOREIGN KEY(source_account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    CONSTRAINT fk_destination_account FOREIGN KEY(destination_account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    source_account_id UUID NOT NULL,
    destination_id UUID,
    amount MONEY NOT NULL,
    datetime TIMESTAMP DEFAULT (now()) NOT NULL,
    reason VARCHAR(100),

    CONSTRAINT fk_source_account FOREIGN KEY(source_account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    CONSTRAINT fk_destination_entity FOREIGN KEY(destination_id) REFERENCES entities(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS paychecks (
    id SERIAL PRIMARY KEY,
    source_id UUID NOT NULL,
    account_id UUID NOT NULL,
    amount MONEY NOT NULL,
    date DATE DEFAULT CURRENT_DATE,

    CONSTRAINT fk_source_entity FOREIGN KEY(source_id) REFERENCES entities(id) ON DELETE SET NULL,
    CONSTRAINT fk_destination_account FOREIGN KEY(account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

