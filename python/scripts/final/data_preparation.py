import pandas as pd
import numpy as np


def compute_base_prices(daily_stays: pd.DataFrame) -> pd.Series:
    """Average price per bed for each apartment, over all booked days (p̄_a)."""
    return daily_stays.groupby('apartment_id')['nightly_bed_rate'].mean()


def compute_relative_price_index(daily_stays: pd.DataFrame, base_prices: pd.Series) -> pd.Series:
    """
    Beds-sold-weighted average of each apartment's price relative to its base price (r_t).

    r_t = sum_a [ y_{a,t} * (p_{a,t} / p_bar_a) ] / sum_a y_{a,t}

    Only defined for days with at least one booking.
    """
    stays = daily_stays.copy()
    stays['price_relative_to_base'] = stays['nightly_bed_rate'] / stays['apartment_id'].map(base_prices)
    stays['beds_weighted_relative_price'] = stays['price_relative_to_base'] * stays['beds_count']

    numerator = stays.groupby('stay_date')['beds_weighted_relative_price'].sum()
    denominator = stays.groupby('stay_date')['beds_count'].sum()
    return (numerator / denominator).rename('relative_price_index')


def compute_occupancy_rate(daily_stays: pd.DataFrame, total_capacity: int) -> pd.Series:
    """Daily fraction of total beds sold across the segment (o_t)."""
    return (daily_stays.groupby('stay_date')['beds_count'].sum() / total_capacity).rename('occupancy_rate')


def build_historical_sample(occupancy_rate: pd.Series, relative_price_index: pd.Series) -> pd.DataFrame:
    """
    Join occupancy rates and relative price indices into the historical sample
    D = {(o_t, r_t)}. Days where either value is missing are dropped.
    """
    return pd.DataFrame({
        'occupancy_rate': occupancy_rate,
        'relative_price_index': relative_price_index,
    }).dropna()


def prepare_full_occupancy_series(
    daily_stays: pd.DataFrame,
    total_capacity: int,
    start_date: str,
    end_date: str,
) -> pd.Series:
    """
    Daily occupancy rate over the full analysis period, with zero on unbooked days.
    Used as input to SARIMA (requires a complete, gap-free time series).
    end_date is exclusive.
    """
    daily_beds_sold = daily_stays.groupby('stay_date')['beds_count'].sum()

    full_range = pd.date_range(
        start=pd.Timestamp(start_date),
        end=pd.Timestamp(end_date) - pd.Timedelta(days=1),
        freq='D',
    )
    occupancy = daily_beds_sold.reindex(full_range, fill_value=0) / total_capacity
    occupancy.index.freq = 'D'
    return occupancy.rename('occupancy_rate')
