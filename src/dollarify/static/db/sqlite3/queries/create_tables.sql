CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT uuid_generate_v4(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    password VARCHAR(128) NOT NULL,
    phone VARCHAR(15),
    PRIMARY KEY (id)
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
    id SERIAL PRIMARY KEY,
    name VARCHAR(32),
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS accounts (
    id UUID DEFAULT uuid_generate_v4(),
    account_type_id INTEGER NOT NULL,
    provider_id INTEGER,

    CONSTRAINT fk_type FOREIGN KEY(account_type_id) REFERENCES account_types(id) ON DELETE RESTRICT,
    CONSTRAINT fk_provider FOREIGN KEY(provider_id) REFERENCES entities(id) ON DELETE RESTRICT

);
