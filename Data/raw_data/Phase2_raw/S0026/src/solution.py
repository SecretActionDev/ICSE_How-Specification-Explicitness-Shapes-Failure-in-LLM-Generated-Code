from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities,
    with the constraint that at least one resource must remain unallocated.

    Raises:
        TypeError: If inputs are of wrong type.
        ValueError: If numeric values are invalid (negative, NaN, or infinite), or if request uses unknown resource.
    """
    # Type checks for main inputs
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if not resources:
        raise ValueError("Resources dictionary cannot be empty")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")

    # Validate resource keys and values
    for r_key, r_value in resources.items():
        if not isinstance(r_key, str):
            raise TypeError("Resource keys must be strings")
        if not isinstance(r_value, (int, float)):
            raise TypeError("Resource values must be numbers")
        if r_value < 0 or math.isnan(r_value) or math.isinf(r_value):
            raise ValueError("Resource values must be non-negative, finite numbers")

    # Validate each request
    for request in requests:
        if not isinstance(request, dict):
            raise TypeError("Each request must be a dictionary")
        for req_key, req_value in request.items():
            if not isinstance(req_key, str):
                raise TypeError("Request keys must be strings")
            if not isinstance(req_value, (int, float)):
                raise TypeError("Request values must be numbers")
            if req_value < 0 or math.isnan(req_value) or math.isinf(req_value):
                raise ValueError("Request values must be non-negative, finite numbers")
            if req_key not in resources:
                raise ValueError(f"Request uses unknown resource '{req_key}'")

    # Calculate total demand
    total_demand = {}
    for request in requests:
        for r_key, r_value in request.items():
            total_demand[r_key] = total_demand.get(r_key, 0) + r_value

    # Check if any resource exceeds capacity
    for r_key, r_capacity in resources.items():
        if total_demand.get(r_key, 0) > r_capacity:
            return False

    # Check new requirement: at least one resource must remain unallocated
    all_fully_used = all(total_demand.get(r_key, 0) == r_capacity for r_key, r_capacity in resources.items())
    if all_fully_used:
        return False

    return True