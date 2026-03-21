DDL = """

CREATE TABLE Company (
        ticker VARCHAR(5),
        name VARCHAR(100),
        industry VARCHAR(20),
        sector VARCHAR(20),
        country VARCHAR(20),
        earning_per_share DECIMAL(15, 2),
        revenue DECIMAL(15, 2),
        net_income DECIMAL(15, 2), 
        total_assets DECIMAL(15, 2),
        total_debts DECIMAL(15, 2),
        PRIMARY KEY (ticker)
    
);

CREATE TABLE Stock (
        date DATE,
        ticker VARCHAR(5),
        adj_close DECIMAL(10,6),
        close_price DECIMAL(10,6),
        volume BIGINT,
        open_price DECIMAL(10,6),
        high_price DECIMAL(10,6),
        low_price DECIMAL(10,6),
        PRIMARY KEY (date, ticker)
        FOREIGN KEY (ticker) REFERENCES Company(ticker)
);

CREATE TABlE News (
	id VARCHAR(30),
	date DATE,
	url VARCHAR(255),
	source VARCHAR(50),
	tone DECIMAL(15, 3),
	negative_score DECIMAL(15, 3),
	positive_score DECIMA(15, 3),
	polarity DECIMAL(15, 3),
	PRIMARY KEY (id)
);

CREATE TABlE Covers (
	ticker VARCHAR(5),
	news_id VARCHAR(30),
	PRIMARY KEY (ticker, news_id)
	FOREIGN KEY (ticker) REFERENCES Company(ticker)
	FOREIGN KEY (news_id) REFERENCES News(id)
);

"""
