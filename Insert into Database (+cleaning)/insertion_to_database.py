import pandas as pd
import psycopg2
import os

import config
# Database connection parameters
DB_NAME = os.getenv("DB_NAME")  
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# File path for your Parquet file
PARQUET_FILE_PATH = config.news("News_embeddings_with_headlines2_final.parquet")

# Connect to PostgreSQL database
def connect_to_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Initialize database connection
conn = connect_to_db()
cursor = conn.cursor()

# Ensure `pgvector` extension is enabled
try:
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()
    print("pgvector extension ensured.")
except Exception as e:
    print(f"Error ensuring pgvector extension: {e}")
    conn.rollback()

# Create the table with an embedding column
create_table_query = """
CREATE TABLE IF NOT EXISTS news (
    id BIGINT PRIMARY KEY,
    link TEXT NOT NULL,
    date DATE NOT NULL,
    category VARCHAR(20),
    headline TEXT,
    short_description TEXT,
    content TEXT,
    embedding VECTOR(768)
);
"""
try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Table created successfully.")
except Exception as e:
    print(f"Error creating table: {e}")
    conn.rollback()

# Read the entire Parquet file
try:
    print("Loading Parquet file...")
    df = pd.read_parquet(PARQUET_FILE_PATH, engine="pyarrow")
    print(f"Loaded Parquet file with {len(df)} rows.")
except Exception as e:
    print(f"Error loading Parquet file: {e}")
    cursor.close()
    conn.close()
    exit()

# Insert all rows in one transaction
try:
    insert_query = """
        INSERT INTO news (id, link, date, category, headline, short_description, content, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    rows_to_insert = [
        (
            row["id"],
            row["link"],
            row["date"],
            row["category"],
            row["headline"],
            row["short_description"],
            row["content"],
            row["embedding"]
        )
        for _, row in df.iterrows()
    ]
    print("Inserting rows...")
    cursor.executemany(insert_query, rows_to_insert)
    conn.commit()
    print(f"Successfully inserted {len(rows_to_insert)} rows.")
except Exception as e:
    conn.rollback()
    print(f"Error inserting rows: {e}")
finally:
    cursor.close()
    conn.close()

print("Data upload complete.")
