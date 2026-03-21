import pandas as pd
import numpy as np

CSV_FILE_PATH = "/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_with_embeddings_final.csv"
df = pd.read_csv(CSV_FILE_PATH)

# Check the data type of each embedding in the column
print(df['embedding'].apply(type).value_counts())
"""



def validate_embedding(embedding, expected_dim=512):
    # Check if the embedding is a NumPy array
    if isinstance(embedding, np.ndarray):
        # Check the dimension of the array
        if embedding.shape[0] != expected_dim:
            return "Incorrect Dimension"
        # Check if all elements are numeric (int or float)
        if not np.issubdtype(embedding.dtype, np.number):
            return "Non-Numeric Data"
        return "Valid"
    return "Invalid Format"

# Apply the validation function
# Apply the validation function to the embedding column
df['embedding_status'] = df['embedding'].apply(validate_embedding)

# Check validation summary
print(df['embedding_status'].value_counts())

# Inspect rows with errors (if any)
invalid_embeddings = df[df['embedding_status'] != 'Valid']
print(f"Number of invalid embeddings: {len(invalid_embeddings)}")
print(invalid_embeddings.head())

"""