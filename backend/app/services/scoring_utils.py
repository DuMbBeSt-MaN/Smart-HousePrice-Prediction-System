# app/services/scoring_utils.py

def normalize(value, max_value=10):
    """
    Normalizes values to 0–1 range
    """
    if value is None:
        return 0.0
    return min(value / max_value, 1.0)


def inverse_normalize(value, max_value=10):
    """
    For risk metrics (lower is better)
    """
    if value is None:
        return 1.0
    return 1.0 - min(value / max_value, 1.0)