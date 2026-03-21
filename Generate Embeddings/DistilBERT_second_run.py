import pandas as pd
import torch
from transformers import DistilBertModel, DistilBertTokenizer
import numpy as np
from tqdm import tqdm

# Load your data
file_path = '/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_v3_cleaned.csv'
df = pd.read_csv(file_path)
descriptions = df['short_description'].tolist()

# Set batch size
batch_size = 512
# Ensure all items in batch_texts are strings
descriptions = [str(text) for text in descriptions]  # Convert each entry to a string

# Load the model and tokenizer
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Set device to MPS if available, otherwise default to CPU
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = model.to(device)
print(f"Using device: {device}")

# Initialize a list to track failed batches
failed_batches = []

# Define output path and set `write_header` to True for the first write
output_path = '/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_with_embeddings.csv'
write_header = True

# Process the descriptions in batches
for i in tqdm(range(0, len(descriptions), batch_size)):
    batch_texts = descriptions[i:i+batch_size]  # Get a batch of descriptions
    try:
        # Tokenize and move inputs to the device
        inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(device)

        # Generate embeddings for the batch
        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].detach()
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        
        # Move embeddings to CPU and convert to a list of numpy arrays
        batch_embeddings = embeddings.cpu().numpy()
        
        # Create a DataFrame for the current batch
        batch_df = df.iloc[i:i+batch_size].copy()
        batch_df['embedding'] = list(batch_embeddings)
        
        # Append batch DataFrame to CSV
        batch_df.to_csv(output_path, mode='a', header=write_header, index=False)
        
        # Set header to False after the first write
        write_header = False
    
    except Exception as e:
        # Log the batch number in case of an error
        failed_batches.append(i // batch_size)
        print(f"Error processing batch {i // batch_size}: {e}")

# Output the failed batches if any
if failed_batches:
    print(f"The following batches encountered errors and were skipped: {failed_batches}")
else:
    print("All batches processed successfully.")
