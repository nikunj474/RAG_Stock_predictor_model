import pandas as pd
import os
import re
import requests

import config

os.chdir(str(config.DATA_DIR / "helpful"))

#check memory usage
'''
sample = pd.read_csv("news_data.csv", nrows=1000)
print(sample.memory_usage(deep=True).sum() / 1000)  # Average memory per row
'''

# Define the chunk size (number of rows per chunk)
chunksize = 10000  # Adjust based on memory availability

# Initialize an empty list to store processed chunks if you need to combine them
processed_chunks = []

# List to store invalid URLs
invalid_urls = []

# Date conversion function
def convert_to_datetime(date_str):
    # Remove the trailing decimal if it exists
    date_str = str(date_str).split('.')[0]
    # Extract the components
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]
    hour = date_str[8:10]
    minute = date_str[10:12]
    second = date_str[12:14]
    # Format as SQL DATETIME (YYYY-MM-DD HH:MM:SS)
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"

# Function to split V2Tone column into individual components
def split_v2tone(v2tone_str):
    if pd.notnull(v2tone_str):
        # Split by comma
        parts = v2tone_str.split(',')
        # Convert parts to float if they exist, else use None
        return [float(parts[i]) if i < len(parts) else None for i in range(7)]
    else:
        return [None] * 7
'''
# Function to check if URL is reachable
def is_reachable_url(url):
    try:
        response = requests.head(url, timeout=5)  # Sends a head request
        return response.status_code == 200  # Returns True if the status is 200 (OK)
    except requests.RequestException:
        return False
'''
# Loop over each chunk
for chunk in pd.read_csv("news_data.csv", chunksize=chunksize):
    # Select only the desired columns
    columns_to_keep = ['GKGRECORDID', 'DATE', 'SourceCommonName', 'DocumentIdentifier',  'V2Tone']
    chunk = chunk[columns_to_keep]

    # Drop null values (optional)
    chunk = chunk.dropna()

    # Convert the DATE column to SQL DATETIME format
    chunk['DATE'] = chunk['DATE'].apply(convert_to_datetime)

    # Split the V2Tone column into separate columns
    tone_columns = ['Tone', 'Positive_Score', 'Negative_Score', 'Polarity', 'Activity_Reference_Density', 'Self_Group_Reference_Density', 'Unknown_V2Tone_Field']
    chunk[tone_columns] = chunk['V2Tone'].apply(lambda x: pd.Series(split_v2tone(x)))

    # Drop the original V2Tone column if you no longer need it
    chunk = chunk.drop(columns=['V2Tone', 'Activity_Reference_Density', 'Self_Group_Reference_Density', 'Unknown_V2Tone_Field'])

    ''' 
    # Check each URL in the DocumentIdentifier column and collect invalid URLs
    is_valid_url = chunk['DocumentIdentifier'].apply(lambda url: is_reachable_url(url))
    invalid_urls.extend(chunk.loc[~is_valid_url, 'DocumentIdentifier'])  # Add invalid URLs to the list

    # Filter out rows with invalid URLs
    chunk = chunk[is_valid_url]
    '''

    print(chunk.head())
    # Print the iteration we are on out of total chunks
    total_rows = 1500000
    current_chunk = len(processed_chunks) + 1
    total_chunks = total_rows // chunksize + (1 if total_rows % chunksize != 0 else 0)
    print(f"Processing chunk {current_chunk} out of {total_chunks}")

    # Add the processed chunk to the list
    processed_chunks.append(chunk)
    # Save the processed data to a new CSV file
    chunk.to_csv('processed_data_clean.csv', mode='a', header=False, index=False)

    # Print the number of invalid URLs and break after the first chunk to test
    #print("Number of invalid URLs:", len(invalid_urls))
