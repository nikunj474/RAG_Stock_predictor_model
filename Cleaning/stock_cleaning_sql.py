import pandas as pd
import os

os.chdir('/Users/nsusser/Desktop/Github/yfinance/Data/stocks/')


# Step 1: Load the CSV file into a DataFrame
df = pd.read_csv("ticker_data2012.csv")

# Rename columns to align with DDL schema
column_mapping = {
    'Date': 'date',
    'Ticker': 'ticker',
    'Adj Close': 'adj',
    'Close': 'close',
    'High': 'high',
    'Low': 'low',
    'Open': 'open',
    'Volume': 'volume'
}
df = df.rename(columns=column_mapping)

# Convert `date` column to DATE format (without time)
df['date'] = pd.to_datetime(df['date']).dt.date

# Check min, max, and average values for each numeric column
numeric_columns = ['adj', 'close', 'open', 'high', 'low', 'volume']
summary_stats = {}

for column in numeric_columns:
    min_value = df[column].min()
    max_value = df[column].max()
    avg_value = df[column].mean()
    
    # Store the results
    summary_stats[column] = {
        "min": min_value,
        "max": max_value,
        "average": avg_value
    }

# Print the summary statistics
print("Summary Statistics for Numeric Columns:")
for column, stats in summary_stats.items():
    print(f"\nColumn '{column}':")
    print(f"  Minimum value: {stats['min']}")
    print(f"  Maximum value: {stats['max']}")
    print(f"  Average value: {stats['average']}")

# Define a function to count decimal places
def count_decimal_places(value):
    if pd.notnull(value):
        # Split by the decimal point and count digits after it
        parts = str(value).split('.')
        if len(parts) > 1:
            return len(parts[1])  # Count of digits after the decimal point
    return 0  # No decimal places if there's no decimal part

# Columns to check for decimal places
columns_to_check = ['adj', 'close', 'open', 'high', 'low', 'volume']

# Dictionary to store min, max, and average decimal places for each column
decimal_places_info = {}

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

# Check if all decimal places in the 'volume' column are zero
# Extract the decimal part of each 'volume' entry by subtracting the integer part
decimal_part_non_zero = df['volume'] % 1 != 0  # This checks if the decimal part is non-zero

# Count how many rows have a non-zero decimal part in 'volume'
non_zero_decimal_count = decimal_part_non_zero.sum()

# Print results
if non_zero_decimal_count == 0:
    print("All volume values have 0 as the decimal.")
else:
    print(f"{non_zero_decimal_count} volume values have a non-zero decimal.")
# Convert the 'volume' column to integer
df['volume'] = df['volume'].astype(int)


# Step 1: Check for `NaN` or `NULL` values in each column
# Print the count of missing values in each column
missing_values = df.isnull().sum()
print("\nColumns with Missing Values:")
print(missing_values[missing_values > 0])

# Step 2: Drop rows with any `NaN` values
df = df.dropna()

# Step 3: Check and enforce data types to match the DDL
# Define the expected data types based on the DDL
expected_dtypes = {
    'date': 'datetime64[ns]',  # For DATE column
    'ticker': 'string',        # VARCHAR(5)
    'adj': 'float',            # DECIMAL(20, 16) compatible with float in pandas
    'close': 'float',
    'open': 'float',
    'high': 'float',
    'low': 'float',
    'volume': 'int64'          # BIGINT
}

# Convert the 'date' column to DATE format (without time component)
df['date'] = pd.to_datetime(df['date']).dt.date

# Convert each column to the expected data type
for column, dtype in expected_dtypes.items():
    df[column] = df[column].astype(dtype)

# Verify the data types after conversion
print("\nData Types After Conversion:")
print(df.dtypes)

# Save the cleaned data back to CSV or load it into the SQL database
df.to_csv("cleaned_stock_data2012.csv", index=False)
print("\nData has been cleaned, NaNs removed, types enforced, and saved to 'cleaned_stock_data2012.csv'")
