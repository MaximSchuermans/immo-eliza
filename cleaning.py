import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv('data/immoweb_data.csv')  # replace with your file

# Remove rows where the 'price' column is NaN (empty)
df = df.dropna(subset=['Price'])

# Step 1: Handle missing values

# Replace tuples like `(None,)` with actual None/NaN values
#df.replace({"(None,)": None}, inplace=True)
#df.replace({"(1,)": 1}, inplace=True)
# Replace NaN with "Missing Data" for all columns
#df.fillna("-1", inplace=True)

# Step 2: Convert boolean-like columns to consistent True/False
boolean_columns = ['Fully_Equipped_Kitchen', 'Furnished', 'Open_fire', 'Swimming_Pool']
for col in boolean_columns:
    df[col] = df[col].replace({False: 0, True: 1}).fillna(0)  # Convert 0/1 to False/True, fill empty values with False

# Step 3: Convert data types
columns_to_convert = ['Price', 'Number_of_Rooms', 'Living_Area', 'Furnished', 'Open_fire', 'Terrace', 'Terrace_Area', 'Garden_Area', 'Surface_of_the_Land', 'Surface_area_plot_of_land', 'Number_of_Facades', "Swimming_Pool"]  

for col in columns_to_convert: 
    #df[col] = df[col].astype(int)
    #df[[col]].astype('int32')
    #df[[col]] = df[[col]].apply(lambda x : int(x))
    df[[col]] = df[[col]].map(lambda x: int(x), na_action='ignore')

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
print(df.dtypes)

# Optional: Save cleaned data to a new CSV file
output_path = "data/cleaned_data.csv"
df.to_csv(output_path, index=False)
print(f"Cleaned data saved to {output_path}")
