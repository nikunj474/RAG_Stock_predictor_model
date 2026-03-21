import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np

# Load the Parquet file
parquet_path = "/Users/nsusser/Desktop/Github/yfinance/Data/news/News_embeddings_with_headlines2.parquet"
df = pd.read_parquet(parquet_path)

# Check the structure of the DataFrame
print("Initial DataFrame:")
print(df.head())

# Convert embeddings to PostgreSQL array format
def embedding_to_pgvector(embedding):
    if isinstance(embedding, (list, np.ndarray)):
        return str(list(embedding)).replace(" ", "")  # Convert to '[1,2,3]' format
    elif isinstance(embedding, str):
        try:
            # Safely convert string to list, then format
            embedding_array = eval(embedding)
            return str(list(embedding_array)).replace(" ", "")
        except Exception as e:
            print(f"Error converting embedding: {embedding} | Error: {e}")
            return None  # Handle invalid embeddings
    else:
        return None  # Handle unexpected formats

# Apply the conversion
df['pgvector_embedding'] = df['embedding'].apply(embedding_to_pgvector)

# Verify the result
print("\nConverted Embeddings (pgvector format):")
print(df[['pgvector_embedding']].head())

# Ensure 'date' is in datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert to datetime, handling errors
if df['date'].isnull().any():
    print("Warning: Some dates could not be converted and are now NaT!")

# Drop unwanted columns and reorder
df = df.drop(columns=['authors'], errors='ignore')  # Drop 'authors' if it exists
new_order = ['index', 'link', 'date', 'category', 'headline', 'short_description', 'combined_text', 'pgvector_embedding']
df = df[new_order]
df.rename(columns={'index': 'id', 'combined_text': 'content', 'pgvector_embedding': 'embedding'}, inplace=True)

# Verify column types and structure
print("\nColumn Data Types After Transformation:")
print(df.dtypes)

# Print actual Python types of column elements
print("\nElement Type Inspection:")
for column in df.columns:
    first_element = df[column].iloc[0]
    print(f"{column}: {type(first_element)}")

# Save the transformed DataFrame to a new Parquet file
final_parquet_path = "/Users/nsusser/Desktop/Github/yfinance/Data/news/News_embeddings_with_headlines2_final.parquet"
table = pa.Table.from_pandas(df)  # Convert DataFrame to Arrow Table
pq.write_table(table, final_parquet_path)

print(f"\nTransformed DataFrame successfully saved to {final_parquet_path}")

# Validate embeddings
def validate_embedding(embedding):
    if isinstance(embedding, str):
        try:
            # Safely evaluate the string to a Python list
            embedding = eval(embedding)
        except Exception as e:
            print(f"Error evaluating embedding: {embedding} | Error: {e}")
            return False
    if isinstance(embedding, (list, np.ndarray)):
        return len(embedding) == 768
    return False

# Check embedding lengths
embedding_validity = df['embedding'].apply(validate_embedding)
invalid_embeddings = df[~embedding_validity]

# Validate column names and data types
expected_columns = ['id', 'link', 'date', 'category', 'headline', 'short_description', 'content', 'embedding']
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
    print(f"Error: {len(invalid_embeddings)} embeddings are invalid (not 768 elements).")
    print("Sample invalid embeddings:")
    print(invalid_embeddings[['id', 'embedding']].head())
else:
    print("All embeddings are valid with 768 elements.")

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
