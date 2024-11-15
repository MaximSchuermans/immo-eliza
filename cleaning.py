import pandas as pd

# Load your data
df = pd.read_csv('data/immoweb_data.csv')  # replace with your file

# Remove rows where the 'price' column is NaN (empty)
df_cleaned = df.dropna(subset=['Price'])


# Step 1: Handle missing values
# Replace tuples like `(None,)` with actual None/NaN values
df.replace({"(None,)": None}, inplace=True)
df.replace({"(1,)": 1}, inplace=True)
# Replace NaN with "Missing Data" for all columns
#df.fillna("-1", inplace=True)

# Step 2: Convert boolean-like columns to consistent True/False
boolean_columns = ['Fully_Equipped_Kitchen', 'Furnished', 'Open_fire', 'Swimming_Pool']
for col in boolean_columns:
    df[col] = df[col].replace({False: 0, True: 1}).fillna(0)  # Convert 0/1 to False/True, fill empty values with False

# Step 3: Convert data types
# Remove tuple formatting and convert to numeric for certain columns
numeric_columns = ['Terrace_Area', 'Garden_Area', 'Surface_of_the_Land', 'Number_of_Facades']
for col in numeric_columns:
    # Remove tuples and convert to numeric
    df[col] = df[col].astype(str).str.extract(r'(\d+)')[0].astype(float)

# Step 4: Standardize casing in text columns
df['Locality'] = df['Locality'].str.title()
df['Type_of_Property'] = df['Type_of_Property'].str.title()

# Step 5: Drop unnecessary columns
if 'Type_of_Sale' in df.columns:
    df.drop(columns=['Type_of_Sale'], inplace=True)

# Step 6: Drop rows with essential fields missing
# Essential fields to check: price, locality, type_of_property
df.dropna(subset=['Price', 'Locality', 'Type_of_Property'], inplace=True)

# Display cleaned DataFrame
print(df.head())

# Optional: Save cleaned data to a new CSV file
output_path = "cleaned_data.csv"
df.to_csv(output_path, index=False)
print(f"Cleaned data saved to {output_path}")
