# -*- coding: utf-8 -*-
"""WRF INPUT COMBINE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VRtoKJz1_xP1s7Gue5Wot8Ye9Tog8-D3
"""

# Step 1: Install necessary libraries
!pip install pandas openpyxl

# Step 2: Import libraries
import pandas as pd

# Step 3: Load both Excel files directly from the environment (replace with the correct file paths if needed)
# Specify the columns to load
selected_station = ['WIB','AWS IDMA2', 'WRF IDMA2']  # Replace with the actual column names or indices
# Load only the specified columns from the Excel file
df_pred = pd.read_excel('/content/6 Months WRF Results.xlsx', sheet_name="ALL-3DA", usecols=selected_station)

# Actual Meassured Data
df_actual = pd.read_excel('/content/IDMA2.xlsx', sheet_name="Data_Indramayu2")  # Actual data

df_pred.info()

df_actual.info()

# Step 4: Convert 'Tanggal' columns to datetime format for proper merging
df_pred['WIB'] = pd.to_datetime(df_pred['WIB'])
df_actual['WIB'] = pd.to_datetime(df_actual['WIB'])

# Step 5: Merge the two DataFrames on 'Tanggal' with an inner join (only common timestamps)
merged_df = pd.merge(df_pred, df_actual, on='WIB', how='inner', suffixes=('_pred', '_actual'))

# Step 7: Remove rows where any value in the specified columns is 0
# Assuming 'WRF IDMA1' and 'IDMA1' are part of the merged DataFrame
merged_df_clean = merged_df[(merged_df[['WRF IDMA2']] != 0).all(axis=1)]

# Step 8: Remove specific columns
columns_to_drop = ['Day_of_Year_Calculation', 'GHI Measurement', 'DNI measurement','DHI Measurement',  ]  # Replace with the columns you want to delete
merged_df_clean = merged_df_clean.drop(columns=columns_to_drop)

# Step 9: Export the cleaned DataFrame to a new Excel file
output_file_name = 'IDMA2+WRF_3DA.xlsx'
merged_df_clean.to_excel(output_file_name, index=False)

# Step 10: (Optional) Download the merged file if using Google Colab
from google.colab import files
files.download(output_file_name)

merged_df_clean.head(10)