from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities,
    ensuring at least one resource remains unallocated.

    Args:
        resources: Dict[str, Number]
            Mapping from resource name to total available capacity.
        requests: List[Dict[str, Number]]
            List of requests. Each request is a mapping from resource name to the amount required.

    Returns:
        True if allocation is feasible and at least one resource remains unallocated, False otherwise.

    Raises:
        TypeError: If inputs are not of expected type.
        ValueError: If numeric values are invalid (negative, NaN, Inf) or required keys missing.
    """
    # Basic type checks
    if resources is None or not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary.")
    if not resources:
        raise ValueError("Resources dictionary cannot be empty.")
    if requests is None or not isinstance(requests, list):
        raise TypeError("Requests must be a list.")

    # Validate resources
    for key, value in resources.items():
        if not isinstance(key, str) or not key:
            raise TypeError("Resource keys must be non-empty strings.")
        if not isinstance(value, (int, float)):
            raise TypeError(f"Resource value for '{key}' must be a number.")
        if value < 0 or math.isnan(value) or math.isinf(value):
            raise ValueError(f"Resource value for '{key}' must be non-negative, finite, and valid.")

    # Validate requests
    for request in requests:
        if not isinstance(request, dict):
            raise TypeError("Each request must be a dictionary.")
        for key, value in request.items():
            if not isinstance(key, str) or not key:
                raise TypeError("Request keys must be non-empty strings.")
            if key not in resources:
                raise ValueError(f"Request key '{key}' is not in available resources.")
            if not isinstance(value, (int, float)):
                raise TypeError(f"Request value for '{key}' must be a number.")
            if value < 0 or math.isnan(value) or math.isinf(value):
                raise ValueError(f"Request value for '{key}' must be non-negative, finite, and valid.")

    # Calculate total demand for each resource
    total_demand = {key: 0 for key in resources}
    for request in requests:
        for key, value in request.items():
            total_demand[key] += value

    # Check that total demand does not exceed capacity
    for key, demand in total_demand.items():
        if demand > resources[key]:
            return False

    # Ensure at least one resource remains unallocated
    for key, demand in total_demand.items():
        if demand < resources[key]:
            return True

    # All resources fully allocated _ invalid
    return False