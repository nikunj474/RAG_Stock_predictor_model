# yfinance

Data has been uploaded to an AWS RDS instance. All data files are stored locally due to size constraints

Folders structure:

Cleaning--files to clean news and stock datasets for uploading to RDS

Generate Embeddings--DistilBERT files to generate embeddings for news dataset. Progressive iterations labeled. Final run is in main folder titled DistilBERT GPU.

Insertion into Database--Prep to insert the kaggle news dataset into RDS instance.

Play--test files and notebooks for pulling data using API

Files:

DistilBERT_run_gpu.py is a file to run the news dataset on local GPU, Nvidia RTX3090 graphics chip, using cuda library.

HNSW_index.py is SQL code to alter parameter groups to create Heirarchical Navigable Small World Index on the vector database.

S&P500.ipynb is the API call to yfinance to download stock data.

Cleaning_headline_embeddings.py is a collated python file to clean all the data in one go.

Cuda_test.py is a test of the cuda GPU.

ddl.py is first schema design

ddl2.py is second schema design, but not final.

gdelt_pypi_2018_2023.py is API call to gdelt database to pull 20gb of news articles from around the world.

kaggle_news_cleaning.py cleans the kaggle news dataset for DistilBERT processing

test_create_embeddings creates test embeddings for similarity search over the news table in the RDS instance.
