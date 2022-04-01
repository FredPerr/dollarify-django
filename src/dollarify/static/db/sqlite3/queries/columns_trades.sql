(
    user_id VARCHAR(32) NOT NULL, 
    account VARCHAR(32) NOT NULL, 
    ticker VARCHAR(5) NOT NULL, 
    buy_date TEXT NOT NULL, 
    shares INTEGER NOT NULL, 
    buy_value REAL NOT NULL, 
    fees REAL NOT NULL, 
    sell_value REAL, 
    sell_date TEXT
)