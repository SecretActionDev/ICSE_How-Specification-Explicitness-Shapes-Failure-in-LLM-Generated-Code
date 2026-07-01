from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    # --- Type checks for inputs ---
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary.")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list of dictionaries.")
    if resources is None:
        raise TypeError("Resources cannot be None.")
    if requests is None:
        raise TypeError("Requests cannot be None.")
    if not resources:
        raise ValueError("Resources cannot be empty.")

    # --- Validate resources ---
    for res, amount in resources.items():
        if not isinstance(res, str):
            raise TypeError("Resource keys must be strings.")
        if not isinstance(amount, (int, float)):
            raise TypeError("Resource amounts must be numeric.")
        if amount < 0:
            raise ValueError("Resource amounts cannot be negative.")
        if math.isnan(amount) or math.isinf(amount):
            raise ValueError("Resource amounts cannot be NaN or infinite.")

    # --- Validate requests ---
    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("Each request must be a dictionary.")
        for res, amount in req.items():
            if not isinstance(res, str):
                raise TypeError("Request keys must be strings.")
            if res not in resources:
                raise ValueError(f"Resource '{res}' not defined in resources.")
            if not isinstance(amount, (int, float)):
                raise TypeError("Requested amount must be numeric.")
            if isinstance(amount, (list, tuple, dict)):
                raise TypeError("Requested amount cannot be a list, tuple, or dict.")
            if amount < 0:
                raise ValueError("Requested amounts cannot be negative.")
            if math.isnan(amount) or math.isinf(amount):
                raise ValueError("Requested amounts cannot be NaN or infinite.")

    # --- Track allocation ---
    allocation = {res: 0 for res in resources}
    
    for req in requests:
        for res, amount in req.items():
            allocation[res] += amount
            if allocation[res] > resources[res]:
                return False

    return True