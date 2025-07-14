import os
import glob
import pandas as pd

from scripts.static import *


def earnings_to_numbers(earnings :pd.Series) -> pd.Series: 
    return ( 
        earnings
        .fillna(0)
        .astype(str)                          
        .str.replace('Kč', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
        .replace('', '0')
        .astype(float)
        .mul(115) #real price in Halíře
        .round(0)
        .astype(int)
    )

def save_data_frame(df: pd.DataFrame, filename: str):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    output_path = os.path.join(WORKING_DATA_DIR, filename)    
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    df = df.rename(columns={
        'Listing': 'apartment_id',
        '# of adults': 'adults_count',
        '# of children': 'children_count',
        '# of infants': 'infants_count',
        '# of nights': 'nights_count',
        'Start date': 'start_date',
        'End date': 'end_date',
        'Booked': 'booked',
        'Earnings': 'earnings',        
    })
    return df

def combine_original_data(directory: str):
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in directory: {directory}")
    
    data_frames = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(data_frames, ignore_index=True)
    combined_df = rename_columns(combined_df)
    return combined_df
    