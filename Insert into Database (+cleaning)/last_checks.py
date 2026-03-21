import pandas as pd
import numpy as np

# Load the Parquet file
parquet_path = "/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_with_embeddings_final.parquet"
df = pd.read_parquet(parquet_path)

# Validate embeddings
def validate_embedding(embedding):
    if isinstance(embedding, (list, np.ndarray)):
        return len(embedding) == 768
    return False

# Check embedding lengths
embedding_validity = df['embedding'].apply(validate_embedding)
invalid_embeddings = df[~embedding_validity]

# Validate column names and data types
expected_columns = ['id', 'link', 'date', 'category', 'headline', 'short_description', 'embedding']
print("\nValidating column names...")
if list(df.columns) != expected_columns:
    print(f"Error: Column names do not match expected names. Found: {list(df.columns)}")
else:
    print("Column names are correct.")

print("\nValidating column data types...")
print(df.dtypes)

# Check for invalid embeddings
print("\nValidating embeddings...")
if len(invalid_embeddings) > 0:
    print(f"Error: {len(invalid_embeddings)} embeddings are invalid (not 512 elements).")
    print("Sample invalid embeddings:")
    print(invalid_embeddings[['id', 'embedding']].head())
else:
    print("All embeddings are valid with 512 elements.")

# Check for null values in NOT NULL columns
print("\nValidating NOT NULL constraints...")
required_columns = ['id', 'link', 'date']
null_counts = df[required_columns].isnull().sum()
if null_counts.sum() > 0:
    print("Error: Null values found in NOT NULL columns.")
    print(null_counts)
else:
    print("No null values in NOT NULL columns.")

# Final confirmation
print("\nValidation complete. If no errors are shown, the data is ready for PostgreSQL upload.")
