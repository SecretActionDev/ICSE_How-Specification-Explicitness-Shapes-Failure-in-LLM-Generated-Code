from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine if a list of resource requests is feasible given available resources.
    A feasible allocation satisfies all requests without exceeding available resources,
    and at least one resource must remain unallocated.

    Args:
        resources: Mapping of resource names to available capacity (non-negative numbers).
        requests: List of request dictionaries, each mapping resource names to requested quantities.

    Returns:
        True if allocation is feasible and leaves at least one resource unallocated, else False.

    Raises:
        TypeError: if types of inputs are invalid.
        ValueError: if values are negative, NaN, infinite, or reference missing resources.
    """

    # --- Type checks for inputs ---
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")
    if resources is None:
        raise TypeError("Resources cannot be None")
    if requests is None:
        raise TypeError("Requests cannot be None")
    
    if not resources:
        raise ValueError("Resource dictionary cannot be empty")

    # --- Validate resources ---
    for res, qty in resources.items():
        if not isinstance(res, str):
            raise TypeError(f"Resource key '{res}' must be a string")
        if isinstance(qty, bool) or not isinstance(qty, (int, float)):
            raise TypeError(f"Resource '{res}' must be numeric, not {type(qty).__name__}")
        if qty < 0 or math.isnan(qty) or math.isinf(qty):
            raise ValueError(f"Resource '{res}' must be non-negative, finite, and not NaN")

    # --- Empty requests: feasible if at least one resource has positive capacity ---
    if not requests:
        return any(qty > 0 for qty in resources.values())

    # --- Initialize total demand dictionary ---
    total_demand: Dict[str, Number] = {res: 0 for res in resources}

    # --- Sum up all requests ---
    for i, request in enumerate(requests):
        if not isinstance(request, dict):
            raise TypeError(f"Request at index {i} must be a dictionary")
        for res, qty in request.items():
            if not isinstance(res, str):
                raise TypeError(f"Request key '{res}' must be a string")
            if res not in resources:
                raise ValueError(f"Request asks for unknown resource '{res}'")
            if isinstance(qty, bool) or not isinstance(qty, (int, float)):
                raise TypeError(f"Request quantity for '{res}' must be numeric, not {type(qty).__name__}")
            if qty < 0 or math.isnan(qty) or math.isinf(qty):
                raise ValueError(f"Request quantity for '{res}' must be non-negative, finite, and not NaN")
            total_demand[res] += qty

    # --- Check if any request exceeds available resources ---
    for res, demand in total_demand.items():
        if demand > resources[res]:
            return False

    # --- Ensure at least one resource remains unallocated ---
    for res, demand in total_demand.items():
        if resources[res] - demand > 0:
            return True

    # If all resources are exactly consumed, allocation is not feasible
    return False