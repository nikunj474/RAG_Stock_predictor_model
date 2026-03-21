import pandas as pd
import torch
from transformers import DistilBertModel, DistilBertTokenizer
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm
import gc
import os

# Load your data
file_path = '/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_v3_cleaned.csv'
df = pd.read_csv(file_path)
descriptions = [str(text) for text in df['short_description'].tolist()]

# Set batch size and super-batch size
batch_size = 512
super_batch_size = 10  # Adjust this depending on available memory

# Load the model and tokenizer
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = model.to(device)
print(f"Using device: {device}")

# Output folder for super-batch files
output_folder = '/Users/nsusser/Desktop/Github/yfinance/Data/embeddings/processed_batches/'
failed_output_path = '/Users/nsusser/Desktop/Github/yfinance/Data/embeddings/failed_batches.parquet'
os.makedirs(output_folder, exist_ok=True)

# Initialize a list to track failed batches and their data
failed_batches = []
failed_data = []

# Process descriptions in super-batches
for i in tqdm(range(0, len(descriptions), batch_size * super_batch_size)):
    super_batch_dfs = []
    
    # Process each batch within the super-batch
    for j in range(i, min(i + batch_size * super_batch_size, len(descriptions)), batch_size):
        batch_texts = descriptions[j:j+batch_size]
        try:
            # Tokenize and process with the model
            inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(device)
            with torch.no_grad():
                outputs = model(**inputs)
                embeddings = outputs.last_hidden_state[:, 0, :].detach()
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            # Convert embeddings to numpy and create DataFrame
            batch_embeddings = embeddings.cpu().numpy()
            batch_df = df.iloc[j:j+batch_size].copy()
            batch_df['embedding'] = list(batch_embeddings)
            
            # Append to the super-batch DataFrame list
            super_batch_dfs.append(batch_df)
            
            # Clear MPS memory and Python garbage
            del inputs, outputs, embeddings, batch_df
            gc.collect()
            
        except Exception as e:
            # Log the batch number and save data for later processing
            print(f"Error processing batch {j // batch_size}: {e}")
            failed_batches.append(j // batch_size)
            failed_data.extend(df.iloc[j:j+batch_size].to_dict('records'))
    
    # Combine all DataFrames within the super-batch and save
    if super_batch_dfs:
        super_batch_df = pd.concat(super_batch_dfs, ignore_index=True)
        table = pa.Table.from_pandas(super_batch_df)
        super_batch_file = os.path.join(output_folder, f"super_batch_{i // (batch_size * super_batch_size)}.parquet")
        pq.write_table(table, super_batch_file)
        print(f"Super-batch saved to {super_batch_file}")
        
        # Clear memory from the super-batch
        del super_batch_dfs, super_batch_df, table
        gc.collect()

# Save failed data if any
if failed_batches:
    print(f"The following batches encountered errors and were skipped: {failed_batches}")
    failed_df = pd.DataFrame(failed_data)
    failed_table = pa.Table.from_pandas(failed_df)
    pq.write_table(failed_table, failed_output_path)
else:
    print("All batches processed successfully.")
