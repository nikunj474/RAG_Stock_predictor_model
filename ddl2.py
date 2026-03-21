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

CREATE TABLE Stocks (
    date DATE,
    ticker VARCHAR(5),
    adj DECIMAL(20, 16),
    close DECIMAL(20, 16),
    open DECIMAL(20, 16),
    high DECIMAL(20, 16),
    low DECIMAL(20, 16),
    volume BIGINT,  
    PRIMARY KEY (date, ticker),
    FOREIGN KEY (ticker) REFERENCES Company(ticker)
);


CREATE TABlE News (
	id VARCHAR(30),
	date DATE,
    source VARCHAR(50),
	url VARCHAR(255),
	tone DECIMAL(18, 16),
	negative_score DECIMAL(18, 16),
	positive_score DECIMAL(18, 16),
	polarity DECIMAL(18, 16),
	PRIMARY KEY (id)
);

CREATE TABlE Covers (
	ticker VARCHAR(5),
	news_id VARCHAR(30),
	PRIMARY KEY (ticker, news_id)
	FOREIGN KEY (ticker) REFERENCES Company(ticker)
	FOREIGN KEY (news_id) REFERENCES News(id)
);

CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    link TEXT UNIQUE,
    headline TEXT,
    category TEXT,
    short_description TEXT,
    authors TEXT,
    date DATE,
    embedding VECTOR(512)
);


"""
