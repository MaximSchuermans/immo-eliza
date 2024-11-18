import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv('data/immoweb_data.csv')

# Display info, types and first 10 rows
print(df, df.info(), df.dtypes)

# Remove rows where the 'price' column is NaN (empty)
df = df.dropna(subset=['Price']) 

# Convert boolean-like columns to consistent 1/0
df['Fully_Equipped_Kitchen'] = df['Fully_Equipped_Kitchen'].replace({False: 0, True: 1}).fillna(0)

# Drop rows with essential fields missing | Essential fields to check: price, locality, type_of_property
df.dropna(subset=['Price', 'Locality', 'Type_of_Property'], inplace=True) 

# Covert columns to integers
columns_to_convert = ['Price', 
                    'Number_of_Rooms', 
                    'Living_Area', 
                    'Furnished', 
                    'Open_fire', 
                    'Terrace', 
                    'Terrace_Area',
                    'Garden', 
                    'Garden_Area', 
                    'Surface_of_the_Land', 
                    'Surface_area_plot_of_land',
                    'Number_of_Facades',
                    'Swimming_Pool',
                    'Disabled_Access',
                    'Lift' 
                    ]

for col in columns_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

# Save cleaned data to a new CSV file
output_path = "data/cleaned_data.csv"
df.to_csv(output_path, index=False)
print(f"Cleaned data saved to {output_path}")



