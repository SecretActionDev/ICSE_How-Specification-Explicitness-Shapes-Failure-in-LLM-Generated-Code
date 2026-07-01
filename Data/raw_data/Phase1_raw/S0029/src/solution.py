## Student Name: Beckham Gahirwa
## Student ID: 220043782

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to  Determine whether a set of resource requests can be satisfied 
given limited capacities. Take int account any possible constraints. See the lab handout
for full requirements.
"""
    
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
    Determine whether a set of resource requests can be satisfied given limited capacities.

    Args:
        resources : Dict[str, Number], Mapping from resource name to total available capacity.
        requests : List[Dict[str, Number]], List of requests. Each request is a mapping from resource name to the amount required.

    Returns:
        True if the allocation is feasible, False otherwise.

    """
    # TODO: Implement this function
    if not isinstance(resources, dict):
        raise ValueError("resources must be a dict mapping resource name to capacity")
    if not isinstance(requests, list):
        raise ValueError("requests must be a list of request dicts")

    # Validate and normalize capacities
    capacities: Dict[str, float] = {}
    for name, cap in resources.items():
        if not isinstance(name, str):
            raise ValueError("resource names must be strings")
        if not _is_finite_number(cap):
            raise ValueError(f"capacity for resource '{name}' must be a finite number")
        cap_f = float(cap)
        if cap_f < 0:
            raise ValueError(f"capacity for resource '{name}' must be non-negative")
        capacities[name] = cap_f

    totals: Dict[str, float] = {name: 0.0 for name in capacities}

    for req in requests:
        if not isinstance(req, dict):
            # required by your public test
            raise ValueError("each request must be a dict mapping resource name to amount required")

        for name, amount in req.items():
            # Unknown resource => infeasible (public test requires this)
            if name not in capacities:
                return False

            if not _is_finite_number(amount):
                raise ValueError(f"request amount for resource '{name}' must be a finite number")
            amt_f = float(amount)
            if amt_f < 0:
                raise ValueError(f"request amount for resource '{name}' must be non-negative")

            totals[name] += amt_f

            # Early exit; float-friendly (no epsilon games unless the handout says otherwise)
            if totals[name] > capacities[name]:
                return False

    return True
