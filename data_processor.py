import pandas as pd

# Load the dataset
df = pd.read_csv('energy_data.csv')

# Display first few rows to check the data
print("First few rows of the dataset:")
print(df.head())

# Check for missing values in the dataset
print("\nChecking for missing values in the dataset:")
print(df.isnull().sum())

# Separate numeric and categorical columns
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
categorical_columns = df.select_dtypes(include=['object']).columns

# Fill missing values for numeric columns with mean
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Fill missing values for categorical columns with mode (most frequent value)
for col in categorical_columns:
    df[col].fillna(df[col].mode()[0])

# Verify that there are no missing values left
print("\nAfter filling missing values:")
print(df.isnull().sum())

# Save the processed data to a new CSV file
df.to_csv('processed_energy_data.csv', index=False)

print("\nProcessed data has been saved to 'processed_energy_data.csv'.")
