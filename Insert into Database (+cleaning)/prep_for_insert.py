import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np

# Load the Parquet file
parquet_path = "/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_with_embeddings2.parquet"
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

# Check column types
print("\nColumn Data Types Before Transformation:")
print(df.dtypes)

# Ensure 'date' is in datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert to datetime, handling errors
if df['date'].isnull().any():
    print("Warning: Some dates could not be converted and are now NaT!")

# Drop unwanted columns and reorder
df = df.drop(columns=['authors'], errors='ignore')  # Drop 'authors' if it exists
new_order = ['index', 'link', 'date', 'category', 'headline', 'short_description', 'pgvector_embedding']
df = df[new_order]
df.rename(columns={'index': 'id', 'pgvector_embedding' : 'embedding'}, inplace=True)

# Verify column types and structure
print("\nColumn Data Types After Transformation:")
print(df.dtypes)
# Print actual Python types of column elements
print("\nElement Type Inspection:")
for column in df.columns:
    first_element = df[column].iloc[0]
    print(f"{column}: {type(first_element)}")

# Confirm specific column types
print("\nAdditional Checks:")
print(f"Date column type: {df['date'].dtype}")  # Should confirm datetime64[ns]
print(f"Embedding column first element type: {type(df['embedding'].iloc[0])}")

print(df.head())

# Save the transformed DataFrame to a new Parquet file
final_parquet_path = "/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_with_embeddings_final.parquet"
table = pa.Table.from_pandas(df)  # Convert DataFrame to Arrow Table
pq.write_table(table, final_parquet_path)

print(f"\nTransformed DataFrame successfully saved to {final_parquet_path}")
