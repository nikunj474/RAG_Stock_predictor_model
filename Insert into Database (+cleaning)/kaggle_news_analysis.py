import pandas as pd
import numpy as np

import config

# Load the CSV data
file_path = config.news("News_Category_Dataset_with_embeddings2.csv")

df = pd.read_csv(file_path)

# 1. Analyze Data Types
print("Data Types:")
print(df.dtypes)

# 2. Check for Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# 3. Analyze Length of Text Columns
def calculate_length(value):
    if pd.notnull(value):
        return len(str(value))
    return 0

text_columns = ['link', 'headline', 'category', 'short_description', 'authors']
length_info = {}

for column in text_columns:
    column_lengths = df[column].apply(calculate_length)
    length_info[column] = {
        "min_length": column_lengths.min(),
        "max_length": column_lengths.max(),
        "avg_length": column_lengths.mean(),
    }

print("\nLength Analysis:")
for column, stats in length_info.items():
    print(f"Column '{column}':")
    print(f"  Minimum length: {stats['min_length']} characters")
    print(f"  Maximum length: {stats['max_length']} characters")
    print(f"  Average length: {stats['avg_length']:.2f} characters")

# 4. Analyze Date Column
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert to datetime
    print("\nDate Analysis:")
    print(f"  Earliest date: {df['date'].min()}")
    print(f"  Latest date: {df['date'].max()}")
    print(f"  Null dates: {df['date'].isnull().sum()}")

# 5. Analyze Embedding Column
if 'embedding' in df.columns:
    def embedding_dimension(value):
        try:
            return len(eval(value))  # Convert string to list and return dimension
        except:
            return np.nan

    embedding_dimensions = df['embedding'].apply(embedding_dimension)
    print("\nEmbedding Analysis:")
    print(f"  Minimum embedding dimension: {embedding_dimensions.min()}")
    print(f"  Maximum embedding dimension: {embedding_dimensions.max()}")
    print(f"  Average embedding dimension: {embedding_dimensions.mean():.2f}")
    print(f"  Null embeddings: {embedding_dimensions.isnull().sum()}")

# 6. Basic Statistics for Numeric Columns
print("\nNumeric Column Statistics:")
numeric_columns = ['index']  # Add numeric columns if applicable
print(df[numeric_columns].describe())

# 7. Value Counts for Categorical Columns
categorical_columns = ['category', 'authors']
print("\nCategorical Column Value Counts:")
for column in categorical_columns:
    print(f"\nColumn '{column}':")
    print(df[column].value_counts())
