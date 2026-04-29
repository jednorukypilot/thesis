import numpy as np
import pandas as pd
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d


def select_price_quantile(
    price_grid: np.ndarray,
    conditional_pdf: np.ndarray,
    quantile: float,
) -> float:
    """
    Select the relative price recommendation r*_t as the alpha-quantile of the
    conditional distribution f_{R|O}(r | o_hat).

    r*_t = inf { r : F_{R|O}(r | o_hat) >= alpha }

    Parameters:
    - quantile: alpha in (0, 1); higher values select more aggressive (higher) prices
    """
    if not 0 < quantile < 1:
        raise ValueError("Quantile must be strictly between 0 and 1.")

    cdf = cumulative_trapezoid(conditional_pdf, x=price_grid, initial=0)
    cdf = cdf / cdf[-1]

    quantile_interpolator = interp1d(cdf, price_grid, kind='linear')
    return float(quantile_interpolator(quantile))


def recommend_apartment_prices(
    relative_price_recommendation: float,
    base_prices: pd.Series,
) -> pd.Series:
    """
    Convert the relative price recommendation r*_t into apartment-specific
    prices per bed.

    p*_{a,t} = r*_t x p_bar_a

    Parameters:
    - relative_price_recommendation: r*_t from select_price_quantile
    - base_prices: Series of p_bar_a indexed by apartment_id

    Returns a Series of recommended nightly rates per bed, indexed by apartment_id.
    """
    return (base_prices * relative_price_recommendation).rename('recommended_price_per_bed')
