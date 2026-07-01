from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    # Validate resources
    if not resources:
        raise ValueError("Resource dictionary cannot be empty")
    
    for res, qty in resources.items():
        if isinstance(qty, bool) or not isinstance(qty, (int, float)):
            raise TypeError(f"Resource '{res}' must be a numeric value, not {type(qty).__name__}")
        if qty < 0 or math.isnan(qty):
            raise ValueError(f"Resource '{res}' must be non-negative and not NaN")

    # Empty requests are trivially feasible
    if not requests:
        return True

    # Initialize total demand dictionary
    total_demand: Dict[str, Number] = {res: 0 for res in resources}
    
    # Sum up all requests
    for i, request in enumerate(requests):
        if not isinstance(request, dict):
            raise TypeError(f"Request at index {i} must be a dictionary")
        for res, qty in request.items():
            if res not in resources:
                raise ValueError(f"Request asks for unknown resource '{res}'")
            if isinstance(qty, bool) or not isinstance(qty, (int, float)):
                raise TypeError(f"Request quantity for '{res}' must be numeric, not {type(qty).__name__}")
            if qty < 0 or math.isnan(qty):
                raise ValueError(f"Request quantity for '{res}' must be non-negative and not NaN")
            total_demand[res] += qty
    
    # Check if total demand exceeds available resources
    for res, demand in total_demand.items():
        if demand > resources[res]:
            return False
    
    return True