import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d


def estimate_joint_density(
    historical_sample: pd.DataFrame,
    grid_size: int = 100,
):
    """
    Estimate the joint density f_{O,R}(o, r) via 2D Gaussian KDE on the
    historical sample of (occupancy_rate, relative_price_index) pairs.

    Returns:
    - kde: fitted gaussian_kde object
    - occupancy_grid: 1D array of occupancy values (x-axis of the grid)
    - price_grid: 1D array of relative price values (y-axis of the grid)
    - density_grid: 2D array shaped (len(price_grid), len(occupancy_grid))
    """
    occupancy_values = historical_sample['occupancy_rate'].values
    price_values = historical_sample['relative_price_index'].values

    kde = gaussian_kde(np.vstack([occupancy_values, price_values]))

    occupancy_grid = np.linspace(occupancy_values.min(), occupancy_values.max(), grid_size)
    price_grid = np.linspace(price_values.min(), price_values.max(), grid_size)

    grid_o, grid_r = np.meshgrid(occupancy_grid, price_grid)
    density_grid = kde(np.vstack([grid_o.ravel(), grid_r.ravel()])).reshape(grid_o.shape)

    return kde, occupancy_grid, price_grid, density_grid


def extract_conditional_distribution(
    occupancy_grid: np.ndarray,
    price_grid: np.ndarray,
    density_grid: np.ndarray,
    predicted_occupancy: float,
):
    """
    Extract the conditional density f_{R|O}(r | o_hat) at a given predicted occupancy.

    Interpolates the joint density grid along the occupancy axis, then normalises
    the resulting slice to obtain a valid 1D PDF.

    Returns:
    - price_grid: 1D array of relative price values (same as input)
    - conditional_pdf: normalised conditional density, same length as price_grid
    """
    if not (occupancy_grid.min() <= predicted_occupancy <= occupancy_grid.max()):
        raise ValueError(
            f"Predicted occupancy {predicted_occupancy:.4f} is outside the observed range "
            f"[{occupancy_grid.min():.4f}, {occupancy_grid.max():.4f}]."
        )

    slice_at_occupancy = interp1d(occupancy_grid, density_grid, axis=1, kind='linear')
    conditional_density = slice_at_occupancy(predicted_occupancy)

    area = np.trapz(conditional_density, x=price_grid)
    if area <= 0:
        raise ValueError("Conditional density integrates to zero -- check input data.")

    return price_grid, conditional_density / area
