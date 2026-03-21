import pandas as pd

# Load the JSON data into a pandas DataFrame
file_path = '/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_v3.json'
df = pd.read_json(file_path, lines=True)  # 'lines=True' if each line is a separate JSON object

# Convert date column to datetime format if necessary
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 'errors=coerce' converts invalid dates to NaT

# Remove rows with any NaN or Null values
df_cleaned = df.dropna()

df_cleaned.index.name = "index"
# Save the cleaned DataFrame to a CSV file
csv_output_path = '/Users/nsusser/Desktop/Github/yfinance/Data/news/News_Category_Dataset_v3_cleaned.csv'
df_cleaned.to_csv(csv_output_path, index=True)

print(f"Data cleaned and saved successfully to '{csv_output_path}'.")
