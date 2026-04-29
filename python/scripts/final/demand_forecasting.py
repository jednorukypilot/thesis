import numpy as np
import pandas as pd
from pmdarima import auto_arima


def fit_sarima_model(occupancy_series: pd.Series, seasonal_period: int = 7):
    """
    Fit SARIMA to the daily occupancy rate series using auto_arima (AIC selection).

    Parameters:
    - occupancy_series: complete daily series (zeros for unbooked days, not NaN)
    - seasonal_period: periods per season -- 7 captures weekly patterns
    """
    model = auto_arima(
        occupancy_series,
        seasonal=True,
        m=seasonal_period,
        stepwise=True,
        suppress_warnings=True,
        trace=True,
        information_criterion='aic',
    )
    return model


def forecast_occupancy(model, horizon: int) -> np.ndarray:
    """
    Forecast occupancy rates for the next `horizon` days.
    Clips results to [0, 1] -- occupancy is a bounded rate.
    """
    return np.clip(model.predict(n_periods=horizon), 0.0, 1.0)
