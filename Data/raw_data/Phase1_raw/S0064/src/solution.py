from typing import Dict, List
import numbers
import math

def is_allocation_feasible(
    resources: Dict[str, numbers.Number],
    requests: List[Dict[str, numbers.Number]]
) -> bool:
    # Validate types for resources and requests themselves
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary.")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list of dictionaries.")
    if not resources:
        raise ValueError("Resources dictionary cannot be empty.")
    
    # Validate resource keys and values
    for res_name, capacity in resources.items():
        if not isinstance(res_name, str):
            raise TypeError("Resource names must be strings.")
        if not isinstance(capacity, numbers.Number) or isinstance(capacity, bool):
            raise TypeError("Resource capacities must be numeric (int/float).")
        if capacity < 0 or math.isnan(capacity) or math.isinf(capacity):
            raise ValueError("Resource capacities must be non-negative finite numbers.")
    
    # Initialize aggregated usage
    total_allocated = {res_name: 0 for res_name in resources}
    
    # Validate and process requests
    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("Each request must be a dictionary.")
        for res_name, amount in req.items():
            if not isinstance(res_name, str):
                raise TypeError("Request keys must be strings.")
            if res_name not in resources:
                raise ValueError(f"Resource '{res_name}' not defined in resources.")
            if not isinstance(amount, numbers.Number) or isinstance(amount, bool):
                raise TypeError("Request values must be numeric (int/float).")
            if amount < 0 or math.isnan(amount) or math.isinf(amount):
                raise ValueError("Request values must be non-negative finite numbers.")
            total_allocated[res_name] += amount
            if total_allocated[res_name] > resources[res_name]:
                return False  # allocation exceeds capacity
    
    return True