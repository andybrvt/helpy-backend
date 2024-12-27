import pandas as pd
import csv  # Import the CSV module for handling quoting

# Load the CSV file
file_path = '../../data/nlm_data.csv'  # Path to your original CSV file
df = pd.read_csv(file_path)

# Rename the 'Task Type' column to 'task_type' (if needed)
df.rename(columns={'Task Type': 'task_type'}, inplace=True)

# Ensure all entries in the "Request" column are strings (this handles it properly)
df['Request'] = df['Request'].astype(str)

# Optionally, fill in missing or incomplete requests with a default string
df['Request'] = df['Request'].fillna("Unknown Request")

# Print out rows where 'Request' is missing or incomplete (to check for issues)
missing_requests = df[df['Request'].str.strip() == '']
if not missing_requests.empty:
    print("Found incomplete or missing requests:")
    print(missing_requests)

# Save the cleaned data back to a new CSV file in the same 'data' folder
cleaned_file_path = '../../data/cleaned_nlm_data.csv'  # You can specify where to save it
df.to_csv(cleaned_file_path, index=False, quoting=csv.QUOTE_MINIMAL)

print(f"Cleaned CSV saved as '{cleaned_file_path}'")
