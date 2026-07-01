from typing import Dict, List, Union
import math

Number = Union[int, float]

def _is_finite_number(x: object) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities,
    and at least one resource remains unallocated after assignment.

    Raises:
        TypeError: If inputs or resource/request keys/values are of incorrect type.
        ValueError: If numbers are negative, NaN, or infinite, or requests reference unknown resources.
    """
    # ------------------------
    # TYPE CHECKS
    # ------------------------
    if not isinstance(resources, dict):
        raise TypeError("resources must be a dict mapping resource name to capacity")
    if not isinstance(requests, list):
        raise TypeError("requests must be a list of request dicts")
    if not resources:
        raise ValueError("resources dictionary must not be empty")

    # ------------------------
    # VALIDATE RESOURCES
    # ------------------------
    capacities: Dict[str, float] = {}
    for name, cap in resources.items():
        if not isinstance(name, str):
            raise TypeError("resource names must be strings")
        if not _is_finite_number(cap):
            raise ValueError(f"capacity for resource '{name}' must be a finite number")
        cap_f = float(cap)
        if cap_f < 0:
            raise ValueError(f"capacity for resource '{name}' must be non-negative")
        capacities[name] = cap_f

    totals: Dict[str, float] = {name: 0.0 for name in capacities}

    # ------------------------
    # VALIDATE REQUESTS
    # ------------------------
    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("each request must be a dict mapping resource name to amount required")
        for name, amount in req.items():
            if not isinstance(name, str):
                raise TypeError("request keys must be strings")
            if name not in capacities:
                raise ValueError(f"request references unknown resource '{name}'")
            if not _is_finite_number(amount):
                raise ValueError(f"request amount for resource '{name}' must be a finite number")
            amt_f = float(amount)
            if amt_f < 0:
                raise ValueError(f"request amount for resource '{name}' must be non-negative")
            totals[name] += amt_f
            if totals[name] > capacities[name]:
                return False  # allocation exceeds capacity

    # ------------------------
    # NEW REQUIREMENT
    # At least one resource must remain unallocated
    # ------------------------
    if not any(totals[name] < capacities[name] for name in capacities):
        return False

    return True