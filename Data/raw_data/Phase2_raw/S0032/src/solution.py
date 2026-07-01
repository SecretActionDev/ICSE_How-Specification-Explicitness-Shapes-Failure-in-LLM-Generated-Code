from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities,
    with at least one resource remaining partially unallocated.

    Args:
        resources: Dictionary of available resources with their maximum capacities.
        requests: List of dictionaries where each dictionary represents a resource request.

    Returns:
        True if a valid allocation exists, False otherwise.

    Raises:
        TypeError: For invalid types of inputs.
        ValueError: For invalid numeric values (negative, NaN, infinite) or missing resources.
    """

    # Validate resources
    if resources is None:
        raise TypeError("Resources cannot be None")
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if not resources:
        raise ValueError("Resources dictionary cannot be empty")

    for key, value in resources.items():
        if not isinstance(key, str):
            raise TypeError("Resource keys must be strings")
        if not isinstance(value, (int, float)):
            raise TypeError("Resource values must be numbers")
        if value < 0 or math.isnan(value) or math.isinf(value):
            raise ValueError("Resource values must be finite, non-negative numbers")

    # Validate requests
    if requests is None:
        raise TypeError("Requests cannot be None")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")

    used: Dict[str, Number] = {resource: 0 for resource in resources}

    for request in requests:
        if not isinstance(request, dict):
            raise TypeError("Each request must be a dictionary")

        for key, value in request.items():
            if not isinstance(key, str):
                raise TypeError("Request keys must be strings")
            if key not in resources:
                raise ValueError(f"Requested resource '{key}' not found in available resources")
            if not isinstance(value, (int, float)):
                raise TypeError("Request values must be numbers")
            if value < 0 or math.isnan(value) or math.isinf(value):
                raise ValueError("Request values must be finite, non-negative numbers")

            # Accumulate used resources
            used[key] += value
            if used[key] > resources[key]:
                return False

    # At least one resource must remain partially unallocated
    for key, total_used in used.items():
        if total_used < resources[key]:
            return True

    # All resources fully consumed С invalid allocation
    return False