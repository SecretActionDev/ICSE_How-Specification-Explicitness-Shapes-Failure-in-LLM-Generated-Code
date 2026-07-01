from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determines whether all requests can be satisfied simultaneously
    given the available resources, ensuring at least one resource
    remains unallocated.

    Raises:
        TypeError: For invalid types (non-numeric, booleans, strings)
        ValueError: For negative numbers, NaNs, infinities, or unknown resources
    """

    # Validate types of inputs
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")

    if resources is None or len(resources) == 0:
        raise ValueError("Resources cannot be empty or None")
    
    # Validate each resource key/value
    for r, cap in resources.items():
        if not isinstance(r, str):
            raise TypeError(f"Resource key must be string, got {type(r).__name__}")
        if isinstance(cap, bool):
            raise TypeError(f"Resource '{r}' cannot be a boolean")
        if not isinstance(cap, (int, float)):
            raise TypeError(f"Resource '{r}' must be a number, got {type(cap).__name__}")
        if cap < 0 or math.isnan(cap) or math.isinf(cap):
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
            if not isinstance(res, str):
                raise TypeError(f"Request key must be string, got {type(res).__name__}")
            if res not in resources:
                raise ValueError(f"Request at index {idx} references unknown resource '{res}'")
            if isinstance(amt, bool):
                raise TypeError(f"Request at index {idx}, resource '{res}' cannot be boolean")
            if not isinstance(amt, (int, float)):
                raise TypeError(f"Request at index {idx}, resource '{res}' must be a number, got {type(amt).__name__}")
            if amt < 0 or math.isnan(amt) or math.isinf(amt):
                raise ValueError(f"Request at index {idx}, resource '{res}' has invalid amount: {amt}")
            if isinstance(amt, (list, tuple, dict)):
                raise TypeError(f"Request at index {idx}, resource '{res}' cannot be a list, tuple, or dict")

            aggregated_demand[res] += amt

    # Check if any aggregated demand exceeds capacity
    for res, total in aggregated_demand.items():
        if total > resources[res]:
            return False

    # Ensure at least one resource remains unallocated
    all_resources_used = all(aggregated_demand[r] >= resources[r] for r in resources)
    if all_resources_used:
        return False

    return True