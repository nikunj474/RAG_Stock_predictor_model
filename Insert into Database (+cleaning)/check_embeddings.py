import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import config

CSV_FILE_PATH = config.news("News_Category_Dataset_with_embeddings2.csv")
df = pd.read_csv(CSV_FILE_PATH)

df = df.drop(columns=['authors'])

# Reorder the remaining columns
new_order = ['index', 'link', 'date', 'category', 'headline', 'short_description', 'embedding']
df = df[new_order]
df.rename(columns={'index': 'id'}, inplace=True)

print(df.columns)
print(df.head())


# Assuming 'df' is your DataFrame
print("Data Types of Columns:")
print(df.dtypes)

parquet_path = config.news("News_Category_Dataset_with_embeddings_final.parquet")
table = pa.Table.from_pandas(df)  # Convert DataFrame to Arrow Table
pq.write_table(table, parquet_path)

print(f"DataFrame successfully saved to {parquet_path}")