import pandas as pd
import os

# Check if the file path is correct
file_path = 'PPP Project Data.xlsx'  # Ensure this file is in the project folder
if os.path.exists(file_path):
    print("File path is correct. Starting to load data.")
else:
    print("File not found. Please check the path.")
    exit()  # Stop execution if the file does not exist

# Load the Excel file
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Preview the first few rows of data to confirm successful loading
print("Initial data preview:")
print(df.head())

# Data cleaning: Remove empty values and clean fields
df = df.dropna(subset=['Project Name', 'Location', 'Project Description'])
df['Location'] = df['Location'].str.strip()

# Create a new keywords field
df['Keywords'] = df['Project Description'].apply(lambda x: ', '.join(x.split()[:5]))

# Export the cleaned data to a JSON file
df.to_json('formatted_data.json', orient='records', lines=True)
print("Data preprocessing completed and exported to JSON file.")
