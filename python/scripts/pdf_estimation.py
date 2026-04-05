import numpy as np
from scipy.stats import gaussian_kde

def create_pdf_estimation(x_data, y_data, grid_size=100):
    """
    Create 2D kernel density estimation from input data.
    
    Parameters:
    - x_data: array-like, x coordinates of data points
    - y_data: array-like, y coordinates of data points  
    - grid_size: int, number of grid points for each dimension
    
    Returns:
    - kde: gaussian_kde object
    - X, Y: meshgrid arrays
    - Z: estimated density values on the grid
    """
    # Stack into 2D array for KDE
    xy = np.vstack([x_data, y_data])
    
    # Fit the 2D kernel density estimator
    kde = gaussian_kde(xy)
    
    # Define grid over the space
    x_grid = np.linspace(x_data.min(), x_data.max(), grid_size)
    y_grid = np.linspace(y_data.min(), y_data.max(), grid_size)
    X, Y = np.meshgrid(x_grid, y_grid)
    positions = np.vstack([X.ravel(), Y.ravel()])
    
    # Compute density values
    Z = kde(positions).reshape(X.shape)
    
    return kde, X, Y, Z