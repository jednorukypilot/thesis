from dataclasses import dataclass

@dataclass
class PredictionData:
    predicted_demand: float
    capacity: int
    elasticity_mean: float
    elasticity_std: float
    revenue: float
