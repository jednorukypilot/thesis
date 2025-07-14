import os
import glob
import pandas as pd

from scripts.static import *

def save_data_frame(df: pd.DataFrame, filename: str):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    output_path = os.path.join(WORKING_DATA_DIR, filename)    
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

def combine_original_data(directory: str):
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in directory: {directory}")
    
    data_frames = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(data_frames, ignore_index=True)
    return combined_df

def load_full_data(directory: str):
    combined_df = combine_original_data(directory)
    return combined_df
    