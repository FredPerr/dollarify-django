INSERT INTO account_types (short_name, full_name, information) VALUES ('CHQ', 'Checking Account', '0.01% Interest Rate;No transactional fee;Not taxed');
INSERT INTO account_types (short_name, full_name, information) VALUES ('HISA', 'High Interest Savings Account', '0.1% Interest Rate;No transactional fee;Not taxed');
INSERT INTO account_types (short_name, full_name, information) VALUES ('CREDIT', 'Credit Account', 'Variable Interest Rate;Variable Cashback or BONUSDOLLARS;Not taxed');
INSERT INTO account_types (short_name, full_name, information) VALUES ('STOCK', 'Stock Market Trading Account', NULL);

INSERT INTO account_attributes (short_name, full_name, information) VALUES('TFSA', 'Tax Free Savings Account', 'No capital gain tax; Prefedined limit of contribution per year by the government; CAN|USA');
INSERT INTO account_attributes (short_name, full_name, information) VALUES('RRSP', 'Registered Retirement Savings Plan', 'No capital gain tax; Delayed taxation on contribution;Predefined or calculated limit of contribution per year; CAN');