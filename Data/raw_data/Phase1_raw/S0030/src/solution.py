## Student Name: Shrey Grover
## Student ID: 219579143

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to  Determine whether a set of resource requests can be satisfied 
given limited capacities. Take int account any possible constraints. See the lab handout
for full requirements.
"""
    
from typing import Dict, List, Union
import math

Number = Union[int, float]


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.

    New requirement (in addition to previous behavior):
      - At least one resource must remain unallocated (i.e., have leftover capacity > 0)
        after fulfilling all requests. If all resources are consumed exactly, allocation
        is NOT feasible.
    """
    EPS = 1e-9  # tolerance for float comparisons

    if not isinstance(resources, dict):
        raise ValueError("resources must be a dict")
    if not isinstance(requests, list):
        raise ValueError("requests must be a list")
    if len(resources) == 0:
        return False

    # ---- Validate resources ----
    for name, cap in resources.items():
        if not isinstance(name, str):
            raise ValueError("resource names must be strings")
        if not isinstance(cap, (int, float)):
            raise ValueError("resource capacities must be numeric")
        if not math.isfinite(float(cap)):
            raise ValueError("resource capacities must be finite")
        if float(cap) < 0:
            return False

    used: Dict[str, float] = {k: 0.0 for k in resources}

    for req in requests:
        if not isinstance(req, dict):
            raise ValueError("each request must be a dict")

        for rname, amount in req.items():
            if not isinstance(rname, str):
                raise ValueError("request resource names must be strings")
            if rname not in resources:
                return False  # unknown resource -> infeasible
            if not isinstance(amount, (int, float)):
                raise ValueError("request amounts must be numeric")
            if not math.isfinite(float(amount)):
                raise ValueError("request amounts must be finite")
            if float(amount) < 0:
                raise ValueError("request amounts must be non-negative")

            used[rname] += float(amount)

    for rname, cap in resources.items():
        if used[rname] > float(cap) + EPS:
            return False

    return any((float(resources[r]) - used[r]) > EPS for r in resources)


