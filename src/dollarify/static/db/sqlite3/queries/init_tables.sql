INSERT OR REPLACE INTO {table_name} (name, information, region) VALUES ('TFSA', 'No capital gain tax;Predefined limit of contribution per year', 'CAN');
INSERT OR REPLACE INTO {table_name} (name, information, region) VALUES ('RRSP', 'Delayed taxation on contribution;Predefined or calculated limit of contribution per year', 'CAN');

INSERT OR REPLACE INTO {table_name} (name, information) VALUES (
    'CHQ', 
    'Checking Account;0.01% Interest Rate;No transactional fee;Not taxed'
);

INSERT OR REPLACE INTO {table_name} (name, information) VALUES (
    'HISA', 
    'High Interest Savings Account;0.1% Interest Rate;No transactional fee;Not taxed'
);

INSERT OR REPLACE INTO {table_name} (name, information) VALUES (
    'CREDIT', 
    'Credit card account;Variable Interest Rate;Variable Cashback or BONUSDOLLARS;Not taxed'
);

INSERT OR REPLACE INTO {table_name} (name, information) VALUES (
    'STOCK', 
    'Credit card account;Variable Interest Rate;Variable Cashback or BONUSDOLLARS;Not taxed'
);