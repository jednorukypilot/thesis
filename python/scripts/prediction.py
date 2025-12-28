import numpy as np

def monte_carlo_revenue(
    predicted_demand,
    capacity,
    elasticity_mean,
    elasticity_std,
    price_factors,
    n_simulations = 1000,
    base_price = 1.0
):
    expected_revenues = []

    for alpha in price_factors:
        # Sample elasticity for this alpha
        random_elasticities = np.random.normal(loc=elasticity_mean, scale=elasticity_std, size=n_simulations)

        # Simulate demand for each sampled elasticity
        simulated_demand = predicted_demand * (alpha ** random_elasticities)

        # Apply capacity constraint
        clipped_demand = np.minimum(simulated_demand, capacity)

        # Compute revenue: price * demand
        simulated_revenue = alpha * base_price * clipped_demand

        # Average over all simulations
        expected_revenue = np.mean(simulated_revenue)
        expected_revenues.append(expected_revenue)

    return np.array(expected_revenues)
