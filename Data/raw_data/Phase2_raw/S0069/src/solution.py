from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    # Basic type checks
    if resources is None:
        raise TypeError("Resources cannot be None")
    if requests is None:
        raise TypeError("Requests cannot be None")
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")
    if len(resources) == 0:
        if len(requests) == 0:
            raise ValueError("Empty resources with empty requests is invalid")
        raise ValueError("Resource dictionary cannot be empty")

    # Validate resource keys and values
    for key, val in resources.items():
        if not isinstance(key, str):
            raise TypeError("Resource keys must be strings")
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError("Resource values must be numbers")
        if val < 0 or math.isnan(val) or math.isinf(val):
            raise ValueError("Resource values must be non-negative finite numbers")

    # Initialize total request tracker
    total_request = {res: 0 for res in resources}

    # Validate each request
    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("Each request must be a dictionary")
        for key, val in req.items():
            if not isinstance(key, str):
                raise TypeError("Request keys must be strings")
            if key not in resources:
                raise ValueError(f"Request uses unknown resource type: {key}")
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise TypeError("Request values must be numbers")
            if val < 0 or math.isnan(val) or math.isinf(val):
                raise ValueError("Request values must be non-negative finite numbers")
            # Check for nested or non-scalar types
            if isinstance(val, (list, tuple, dict)):
                raise TypeError("Request values must be scalar numbers")
            total_request[key] += val

    # Check each resource against capacity
    for res, total in total_request.items():
        if total > resources[res]:
            return False  # exceeds capacity

    # New requirement: at least one resource unit must remain unallocated
    # We allow feasibility if at least one resource has remaining capacity
    any_resource_left = any(resources[res] - total_request[res] > 0 for res in resources)
    if not any_resource_left:
        return False

    return True