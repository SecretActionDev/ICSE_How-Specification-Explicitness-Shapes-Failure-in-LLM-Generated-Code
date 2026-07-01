from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.

    New Requirement:
        At least one unit of some resource must remain unallocated after assignment.

    Args:
        resources: Dictionary mapping resource names (str) to available capacities (int/float).
        requests: List of dictionaries, each mapping resource names to requested amounts (int/float).

    Returns:
        True if a valid allocation exists that satisfies all requests and leaves
        at least one unit of some resource unallocated; False otherwise.

    Raises:
        TypeError: If resources/requests are not proper types, or keys/values are wrong type.
        ValueError: If numeric values are invalid (negative, NaN, Inf) or requests use unknown resources.
    """

    # --- Type checks ---
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")
    if resources is None:
        raise TypeError("Resources cannot be None")
    if requests is None:
        raise TypeError("Requests cannot be None")
    if len(resources) == 0:
        raise ValueError("Resources dictionary cannot be empty")

    # --- Validate resources ---
    for r_key, r_value in resources.items():
        if not isinstance(r_key, str):
            raise TypeError(f"Resource key must be a string: {r_key}")
        if not isinstance(r_value, (int, float)):
            raise TypeError(f"Resource value must be numeric for '{r_key}': {r_value}")
        if r_value < 0 or math.isnan(r_value) or math.isinf(r_value):
            raise ValueError(f"Invalid numeric value for resource '{r_key}': {r_value}")

    total_requested: Dict[str, Number] = {}

    # --- Validate requests ---
    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("Each request must be a dictionary")
        for req_key, req_value in req.items():
            if not isinstance(req_key, str):
                raise TypeError(f"Request key must be string: {req_key}")
            if not isinstance(req_value, (int, float)):
                raise TypeError(f"Request value must be numeric for '{req_key}': {req_value}")
            if req_value < 0 or math.isnan(req_value) or math.isinf(req_value):
                raise ValueError(f"Invalid numeric value in request for '{req_key}': {req_value}")
            if req_key not in resources:
                raise ValueError(f"Request contains unknown resource: '{req_key}'")
            if isinstance(req_value, dict) or isinstance(req_value, list):
                raise TypeError(f"Request value for '{req_key}' cannot be a nested structure")

            total_requested[req_key] = total_requested.get(req_key, 0) + req_value
            if total_requested[req_key] > resources[req_key]:
                return False

    # --- New requirement: at least one resource unallocated ---
    for resource, capacity in resources.items():
        allocated = total_requested.get(resource, 0)
        if allocated < capacity:
            return True  # feasible

    return False  # all resources fully allocated