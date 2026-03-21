import pandas as pd
import os
import re

os.chdir('/Users/nsusser/Desktop/Github/yfinance/')

# Define the chunk size (number of rows per chunk)
chunksize = 1000  # Adjust based on memory availability

# Initialize an empty list to store processed chunks if you need to combine them
processed_chunks = []

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

# Function to clean and convert the specified column into a list
def clean_column(column):
    if pd.notnull(column):
        # Remove enclosing brackets or quotes if present
        column = column.strip("[]\"'")
        # Split by semicolon or comma
        items = [item.split(",")[0].strip() for item in str(column).split(';')]
        # Remove special characters and replace with a space
        items = [re.sub(r'[^a-zA-Z0-9\s]', ' ', item) for item in items]
        # Remove multiple spaces
        items = [re.sub(r'\s+', ' ', item).strip() for item in items]
        # Split by semicolon or comma, then strip whitespace and replace symbols with spaces
        items = [re.sub(r'[_#]', ' ', item).strip() for item in column.split(';')]
        # Replace multiple spaces with a single space and remove any leading or trailing spaces
        items = [re.sub(r'\s+', ' ', item).strip() for item in items]
        return items
    else:
        return []
    
# Function to clean and convert the specified column into a list
def clean_column(column):
    if pd.notnull(column):
        # Split by semicolon or comma, then strip whitespace and symbols
        items = [item.split(",")[0].strip() for item in str(column).split(';')]
        return items
    else:
        return []

# Function to split V2Tone column into individual components
def split_v2tone(v2tone_str):
    if pd.notnull(v2tone_str):
        # Split by comma
        parts = v2tone_str.split(',')
        # Convert parts to float if they exist, else use None
        return [float(parts[i]) if i < len(parts) else None for i in range(7)]
    else:
        return [None] * 7

# Loop over each chunk
for chunk in pd.read_csv("news_data.csv", chunksize=chunksize):
    # Select only the desired columns
    columns_to_keep = ['GKGRECORDID', 'DATE', 'SourceCollectionIdentifier', 'SourceCommonName', 'DocumentIdentifier', 'Themes', 'V2Themes', 'Locations', 'V2Locations', 'Persons', 'V2Persons', 'Organizations', 'V2Organizations', 'V2Tone', 'Dates', 'AllNames']
    chunk = chunk[columns_to_keep]

    # Drop null values (optional)
    chunk = chunk.dropna()

    # Convert the DATE column to SQL DATETIME format
    chunk['DATE'] = chunk['DATE'].apply(convert_to_datetime)

    # Apply the cleaning function to relevant columns
    for column in ['Themes', 'V2Themes', 'Locations', 'V2Locations', 'Persons', 'V2Persons', 'Organizations', 'V2Organizations']:
        chunk[column] = chunk[column].apply(clean_column)

    # Split the V2Tone column into separate columns
    tone_columns = ['Tone', 'Positive_Score', 'Negative_Score', 'Polarity', 'Activity_Reference_Density', 'Self_Group_Reference_Density', 'Unknown_V2Tone_Field']
    chunk[tone_columns] = chunk['V2Tone'].apply(lambda x: pd.Series(split_v2tone(x)))

    # Drop the original V2Tone column if you no longer need it
    chunk = chunk.drop(columns=['V2Tone'])

    # Save the processed data to a new CSV file
    chunk.to_csv('processed_data_11-6.csv', header=True, index=False)

    # Append the processed chunk to a list (optional)
    processed_chunks.append(chunk)

    # Break after processing the first chunk to test
    break
# Optionally, you can view the processed data
print(processed_chunks[0][['Themes', 'V2Themes', 'Locations', 'V2Locations', 'Persons', 'V2Persons', 'Organizations', 'V2Organizations']].head())
