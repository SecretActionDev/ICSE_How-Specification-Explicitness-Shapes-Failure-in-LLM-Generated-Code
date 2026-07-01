from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determines whether all requests can be satisfied simultaneously
    given the available resources.
    
    Raises:
        TypeError: For invalid types (non-numeric, booleans, strings)
        ValueError: For negative numbers, NaNs, or unknown resources
    """

    # Validate resources dictionary
    if not resources:
        raise ValueError("Resources cannot be empty")
    
    for r, cap in resources.items():
        # Disallow boolean values
        if isinstance(cap, bool):
            raise TypeError(f"Resource '{r}' cannot be a boolean")
        # Must be int or float
        if not isinstance(cap, (int, float)):
            raise TypeError(f"Resource '{r}' must be a number, got {type(cap).__name__}")
        # Non-negative
        if cap < 0 or math.isnan(cap):
            raise ValueError(f"Resource '{r}' has invalid capacity: {cap}")

    # Empty requests are trivially feasible
    if not requests:
        return True

    # Initialize aggregated demand
    aggregated_demand: Dict[str, Number] = {r: 0 for r in resources}

    for idx, req in enumerate(requests):
        if not isinstance(req, dict):
            raise TypeError(f"Request at index {idx} is not a dictionary")

        for res, amt in req.items():
            if res not in resources:
                raise ValueError(f"Request at index {idx} references unknown resource '{res}'")
            # Disallow booleans
            if isinstance(amt, bool):
                raise TypeError(f"Request at index {idx}, resource '{res}' cannot be boolean")
            # Must be int or float
            if not isinstance(amt, (int, float)):
                raise TypeError(f"Request at index {idx}, resource '{res}' must be a number, got {type(amt).__name__}")
            # Non-negative and not NaN
            if amt < 0 or math.isnan(amt):
                raise ValueError(f"Request at index {idx}, resource '{res}' has invalid amount: {amt}")

            aggregated_demand[res] += amt

    # Check if any aggregated demand exceeds capacity
    for res, total in aggregated_demand.items():
        if total > resources[res]:
            return False

    return True