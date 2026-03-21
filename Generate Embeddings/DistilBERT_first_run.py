'''import pandas as pd
import torch
from transformers import DistilBertModel, DistilBertTokenizer
import numpy as np

# Load your data
file_path = '/path/to/your/News_Category_Dataset_v3.json'
df = pd.read_json(file_path, lines=True)
descriptions = df['short_description'].tolist()

# Load the model and tokenizer
model = DistilBertModel.from_pretrained(
    "distilbert-base-uncased",
    torch_dtype=torch.float16
)
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Move model to device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Generate embeddings for each short description
all_embeddings = []
batch_size = 32
for i in range(0, len(descriptions), batch_size):
    batch_texts = descriptions[i:i+batch_size]
    inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :].detach()
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

    all_embeddings.extend(embeddings.cpu().numpy())

# Convert list of embeddings to numpy array
all_embeddings_np = np.array(all_embeddings)

# Add embeddings back to the DataFrame
df['embedding'] = list(all_embeddings_np)

# Save to CSV
output_path = '/path/to/News_Category_Dataset_with_embeddings.csv'
df.to_csv(output_path, index=False)
print(f"Embeddings saved to '{output_path}'")'''

'''
import pandas as pd
import torch
from transformers import DistilBertModel, DistilBertTokenizer
import numpy as np

# Load your data
file_path = '/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_v3_cleaned.csv'
df = pd.read_csv(file_path)
descriptions = df['short_description'].tolist()

# Load the model and tokenizer (remove torch_dtype=torch.float16)
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Move model to device (GPU if available)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = model.to(device)
#print(device)

# Set batch size and take only the first batch
batch_size = 512
batch_texts = descriptions[:batch_size]  # Get only the first 32 descriptions

# Tokenize and generate embeddings for the first batch
inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(device)
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].detach()
    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

# Convert the embeddings to a NumPy array
all_embeddings_np = embeddings.cpu().numpy()

# Add embeddings to a subset of the DataFrame
df_subset = df.head(batch_size).copy()
df_subset['embedding'] = list(all_embeddings_np)

# Save the subset to CSV
output_path = '/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_with_embeddings_sample.csv'
df_subset.to_csv(output_path, index=False)
print(f"Sample embeddings saved to '{output_path}'")
'''

'''import pandas as pd
import torch
from transformers import DistilBertModel, DistilBertTokenizer
import numpy as np

# Load your data
file_path = '/path/to/your/News_Category_Dataset_v3.json'
df = pd.read_json(file_path, lines=True)
descriptions = df['short_description'].tolist()

# Load the model and tokenizer
model = DistilBertModel.from_pretrained(
    "distilbert-base-uncased",
    torch_dtype=torch.float16
)
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Move model to device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Generate embeddings for each short description
all_embeddings = []
batch_size = 32
for i in range(0, len(descriptions), batch_size):
    batch_texts = descriptions[i:i+batch_size]
    inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :].detach()
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

    all_embeddings.extend(embeddings.cpu().numpy())

# Convert list of embeddings to numpy array
all_embeddings_np = np.array(all_embeddings)

# Add embeddings back to the DataFrame
df['embedding'] = list(all_embeddings_np)

# Save to CSV
output_path = '/path/to/News_Category_Dataset_with_embeddings.csv'
df.to_csv(output_path, index=False)
print(f"Embeddings saved to '{output_path}'")'''


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

# Initialize an empty list to hold all embeddings and failed batches
all_embeddings = []
failed_batches = []

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
        
        # Move embeddings to CPU and convert to NumPy array for storage
        all_embeddings.extend(embeddings.cpu().numpy())
    
    except Exception as e:
        # Log the batch number in case of an error
        failed_batches.append(i // batch_size)
        print(f"Error processing batch {i // batch_size}: {e}")

# Convert list of embeddings to numpy array
all_embeddings_np = np.array(all_embeddings)

# Add embeddings back to the DataFrame
df['embedding'] = list(all_embeddings_np)

# Save the full DataFrame with embeddings to a CSV file
output_path = '/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_with_embeddings.csv'
df.to_csv(output_path, index=False)
print(f"Embeddings saved to '{output_path}'")

# Output the failed batches if any
if failed_batches:
    print(f"The following batches encountered errors and were skipped: {failed_batches}")
else:
    print("All batches processed successfully.")