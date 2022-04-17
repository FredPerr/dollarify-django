INSERT INTO account_types (short_name, full_name, information) VALUES ('CHQ', 'Checking Account', '0.01% Interest Rate;No transactional fee;Not taxed');
INSERT INTO account_types (short_name, full_name, information) VALUES ('HISA', 'High Interest Savings Account', '0.1% Interest Rate;No transactional fee;Not taxed');
INSERT INTO account_types (short_name, full_name, information) VALUES ('CREDIT', 'Credit Account', 'Variable Interest Rate;Variable Cashback or BONUSDOLLARS;Not taxed');
INSERT INTO account_types (short_name, full_name, information) VALUES ('STOCK', 'Stock Market Trading Account', NULL);

INSERT INTO account_attributes (short_name, full_name, information) VALUES('TFSA', 'Tax Free Savings Account', 'No capital gain tax; Prefedined limit of contribution per year by the government; CAN|USA');
INSERT INTO account_attributes (short_name, full_name, information) VALUES('RRSP', 'Registered Retirement Savings Plan', 'No capital gain tax; Delayed taxation on contribution;Predefined or calculated limit of contribution per year; CAN');

INSERT INTO entities (name, description) VALUES('Government', Null);

INSERT INTO stock_markets (short_name, full_name, timezone, open_hour, close_hour, lunch_break_from, lunch_break_to, holidays) VALUES(
    'NYSE',
    'New York Stock Exchange',
    'EDT',
    9.5,
    4.0,
    Null,
    Null,
    array['22-05-30|Memorial Day', '22-06-20|Juneteenth National Independence Day', '22-07-04|Independence Day', '22-09-05|Labor Day', '22-11-24|Thanksgiving Day', '22-12-26|Christmas Day'] -- ... and so on.
);

INSERT INTO stock_markets (short_name, full_name, timezone, open_hour, close_hour, lunch_break_from, lunch_break_to, holidays) VALUES(
    'TSX',
    'Toronto Stock Exchange',
    'EDT',
    9.5,
    4.0,
    Null,
    Null,
    array['22-05-23|Victoria Day', '22-07-01|Canada Day', '22-08-01|Civic Holiday', '22-09-05|Labor Day', '22-10-10|Thanksgiving Day', '22-12-26|Christmas Day', '22-12-27|Boxing Day'] -- ... and so on.
);

