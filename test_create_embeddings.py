from transformers import DistilBertTokenizer, DistilBertModel
import torch

# Load DistilBERT tokenizer and model
# Load the model and tokenizer
model = DistilBertModel.from_pretrained("distilbert-base-uncased")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
device = torch.device("cpu")
model = model.to(device)
print(f"Using device: {device}")

# Encode the query
query = "Justice Department Probes Server Maker Super Micro Computer. Former employee accused AI server maker of accounting violations. Super Micro Computer is cooperating with the investigation. Their SEC filing is delayed."
inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True)

# Get the embeddings
with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state[:, 0, :].detach()
        embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)



        # Convert the tensor to a list for easier readability
embedding_list = embedding.tolist()
print(embedding_list)
