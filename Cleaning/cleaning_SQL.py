import pandas as pd
import os
import re
import requests

import config

os.chdir(config.news(""))


# Step 1: Load the CSV file into a DataFrame
df = pd.read_csv("processed_data_sql.csv")

'''

# Define a function to count decimal places
def count_decimal_places(value):q
    if pd.notnull(value):
        # Split the number by decimal point and count the digits after it
        parts = str(value).split('.')
        if len(parts) > 1:
            return len(parts[1])  # Count of digits after the decimal point
    return 0  # No decimal places if there's no decimal part

# Initialize dictionary to store min, max, and average decimal places for each column
decimal_places_info = {}

columns_to_check = ['Tone', 'Positive_Score', 'Negative_Score', 'Polarity']

for column in columns_to_check:
    # Calculate decimal places for each value in the column
    decimal_counts = df[column].apply(count_decimal_places)
    
    # Store min, max, and average decimal places
    min_decimals = decimal_counts.min()
    max_decimals = decimal_counts.max()
    avg_decimals = decimal_counts.mean()
    
    decimal_places_info[column] = {
        "min": min_decimals,
        "max": max_decimals,
        "average": avg_decimals
    }

# Print the results
for column, stats in decimal_places_info.items():
    print(f"Column '{column}':")
    print(f"  Minimum decimal places: {stats['min']}")
    print(f"  Maximum decimal places: {stats['max']}")
    print(f"  Average decimal places: {stats['average']:.2f}")



# Columns to check
columns_to_check = ['Tone', 'Positive_Score', 'Negative_Score', 'Polarity']

# Dictionary to store max and min values for each column
value_range_info = {}

for column in columns_to_check:
    max_value = df[column].max()
    min_value = df[column].min()
    value_range_info[column] = {
        "max": max_value,
        "min": min_value
    }

# Print the results
for column, values in value_range_info.items():
    print(f"Column '{column}':")
    print(f"  Maximum value: {values['max']}")
    print(f"  Minimum value: {values['min']}")

# Define a function to calculate the length of each value
def calculate_length(value):
    if pd.notnull(value):
        return len(str(value))  # Convert value to string and get length
    return 0  # Return 0 if the value is null

# Apply the function to calculate the length of each value in both 'url' and 'source' columns
url_lengths = df['url'].apply(calculate_length)
source_lengths = df['source'].apply(calculate_length)

# Calculate min, max, and average length for URLs
min_url_length = url_lengths.min()
max_url_length = url_lengths.max()
avg_url_length = url_lengths.mean()

# Calculate min, max, and average length for sources
min_source_length = source_lengths.min()
max_source_length = source_lengths.max()
avg_source_length = source_lengths.mean()

# Print the results
print("URL Length Analysis:")
print(f"  Minimum length: {min_url_length} characters")
print(f"  Maximum length: {max_url_length} characters")
print(f"  Average length: {avg_url_length:.2f} characters")

print("\nSource Length Analysis:")
print(f"  Minimum length: {min_source_length} characters")
print(f"  Maximum length: {max_source_length} characters")
print(f"  Average length: {avg_source_length:.2f} characters")



# Step 2: Rename the columns to match the database schema
df.columns = [
    'id',            # GKGRECORDID -> id
    'date',          # DATE -> date
    'source',        # SourceCommonName -> source
    'url',           # DocumentIdentifier -> url
    'tone',          # Tone -> tone
    'positive_score',# Positive_Score -> positive_score
    'negative_score',# Negative_Score -> negative_score
    'polarity'       # Polarity -> polarity
]

# Step 3: Convert 'date' column to datetime format (if not already)
df['date'] = pd.to_datetime(df['date'])

# Step 4: Save the DataFrame to a new CSV file
df.to_csv('processed_data_sql.csv', index=False)'''


# Format the date column to remove the time component
df['date'] = pd.to_datetime(df['date']).dt.date
df.to_csv('processed_data_sql.csv', index=False)