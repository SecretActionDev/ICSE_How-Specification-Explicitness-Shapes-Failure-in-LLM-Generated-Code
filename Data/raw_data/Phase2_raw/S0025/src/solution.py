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

    Raises:
        TypeError: If input types are incorrect.
        ValueError: If numeric values are invalid (negative, NaN, or infinite), or request uses undefined resources.

    Returns:
        True if allocation is feasible and leaves at least one resource with unused capacity, False otherwise.
    """

    # --- Type checks ---
    if not isinstance(resources, dict):
        raise TypeError("resources must be a dictionary")
    if not isinstance(requests, list):
        raise TypeError("requests must be a list")
    if resources is None:
        raise TypeError("resources cannot be None")
    if requests is None:
        raise TypeError("requests cannot be None")
    if len(resources) == 0:
        raise ValueError("resources cannot be empty")

    # --- Resource keys and values validation ---
    for r_key, r_val in resources.items():
        if not isinstance(r_key, str):
            raise TypeError(f"resource key must be a string, got {type(r_key)}")
        if not isinstance(r_val, (int, float)):
            raise TypeError(f"resource value must be numeric, got {type(r_val)}")
        if r_val < 0 or math.isnan(r_val) or math.isinf(r_val):
            raise ValueError(f"resource value must be non-negative finite number, got {r_val}")

    # Initialize total demand
    total_demand: Dict[str, Number] = {r: 0 for r in resources}

    # --- Process requests ---
    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("each request must be a dictionary")
        for req_key, req_val in req.items():
            if not isinstance(req_key, str):
                raise TypeError(f"request key must be a string, got {type(req_key)}")
            if req_key not in resources:
                raise ValueError(f"request references undefined resource: {req_key}")
            if not isinstance(req_val, (int, float)):
                raise TypeError(f"request value must be numeric, got {type(req_val)}")
            if req_val < 0 or math.isnan(req_val) or math.isinf(req_val):
                raise ValueError(f"request value must be non-negative finite number, got {req_val}")
            if isinstance(req_val, dict):
                raise TypeError("nested values in requests are not allowed")
            total_demand[req_key] += req_val

    # --- Check feasibility ---
    for r_name, capacity in resources.items():
        if total_demand[r_name] > capacity:
            return False  # exceeds capacity

    # At least one resource must remain unallocated
    for r_name, capacity in resources.items():
        if total_demand[r_name] < capacity:
            return True

    # All resources fully used _ infeasible
    return False