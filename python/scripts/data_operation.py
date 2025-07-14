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
    combined_df = combined_df.drop_duplicates(subset='Confirmation code', keep='first')
    combined_df = rename_columns(combined_df)
    return combined_df

def transform_to_daily_stays(relevant_data: pd.DataFrame) -> pd.DataFrame:
    records = []
    for _, row in relevant_data.iterrows():
        for i in range(row['nights_count']):
            stay_date = row['start_date'] + pd.Timedelta(days=i)
            records.append({
                'stay_date': stay_date, 
                'apartment_id': row['apartment_id'], 
                'price': row['price'], 
                'beds_count': row['beds_count'], 
                'nightly_rate': row['nightly_rate'], 
                'nightly_bed_rate': row['nightly_bed_rate']
                })
            
    df = pd.DataFrame(records)
    df['apartment_bed_rate_pair'] = list(zip(df['apartment_id'], df['nightly_bed_rate']))

    return df

def fill_missing_dates(daily_agg: pd.DataFrame) -> pd.DataFrame:
    full_index = pd.date_range(start=daily_agg.index.min(), end=daily_agg.index.max(), freq='D')

    default_values = {
        'room_nights': 0,
        'occupied_apartments': [],
        'apartment_bed_rate_pairs': [],
        'avg_bed_rate': 0.0,
        'sum_bed_rate': 0.0
    }

    daily_agg = daily_agg.reindex(full_index)
    # daily_agg = daily_agg.fillna(value=default_values)
    daily_agg = daily_agg.reset_index().rename(columns={'index': 'stay_date'})
    return daily_agg