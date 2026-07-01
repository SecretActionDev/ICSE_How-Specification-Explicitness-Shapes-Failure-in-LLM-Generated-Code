from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determines if a set of resource requests can be satisfied 
    given the available resources.

    Args:
        resources (Dict[str, Number]): Available resources {resource_name: capacity}.
        requests (List[Dict[str, Number]]): List of resource requests.

    Returns:
        bool: True if all requests can be satisfied, False otherwise.

    Raises:
        ValueError: If any resource or request has invalid (negative or NaN) values.
    """
    
    # Validate available resources
    for res, val in resources.items():
        if not isinstance(val, (int, float)) or math.isnan(val) or val < 0:
            raise ValueError(f"Invalid resource value for '{res}': {val}")
    
    # Initialize total requested amounts per resource
    total_requested = {res: 0 for res in resources}
    
    # Sum requests for each resource
    for req_index, req in enumerate(requests):
        for res, val in req.items():
            if res not in resources:
                raise ValueError(f"Unknown resource in request {req_index}: {res}")
            if not isinstance(val, (int, float)) or math.isnan(val) or val < 0:
                raise ValueError(f"Invalid request value for '{res}' in request {req_index}: {val}")
            total_requested[res] += val
    
    # Check feasibility
    for res, total in total_requested.items():
        if total > resources[res]:
            return False
    
    return True