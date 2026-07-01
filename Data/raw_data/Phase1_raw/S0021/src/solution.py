# Student Name:
# Student ID:

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to determine whether a set of resource requests can be satisfied
given limited capacities.

Assumptions (reasonable/consistent format):
- `resources` maps resource names to non-negative numeric capacities.
- Each request is a dict mapping resource names to numeric required amounts.
- Requests are interpreted as *simultaneous* (i.e., total demand per resource is the sum across all requests).
- Any resource not present in `resources` has capacity 0 (so any positive request for it makes allocation infeasible).
"""
from typing import Dict, List, Union

Number = Union[int, float]


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.

    Raises:
        ValueError: if inputs are structurally invalid (e.g., a request is not a dict).
    """
    # Structural validation for resources
    if not isinstance(resources, dict):
        raise ValueError(
            "resources must be a dict mapping resource name to capacity")

    for rname, cap in resources.items():
        if not isinstance(rname, str):
            raise ValueError("resource names must be strings")
        if not isinstance(cap, (int, float)):
            raise ValueError(
                f"capacity for resource '{rname}' must be numeric")
        if cap < 0:
            raise ValueError(
                f"capacity for resource '{rname}' cannot be negative")

    # Structural validation for requests
    if not isinstance(requests, list):
        raise ValueError("requests must be a list of dicts")

    total_demand: Dict[str, float] = {}

    for idx, req in enumerate(requests):
        if not isinstance(req, dict):
            raise ValueError(f"request at index {idx} must be a dict")

        for rname, amount in req.items():
            if not isinstance(rname, str):
                raise ValueError("requested resource names must be strings")
            if not isinstance(amount, (int, float)):
                raise ValueError(
                    f"amount for resource '{rname}' in request {idx} must be numeric")
            if amount < 0:
                raise ValueError(
                    f"amount for resource '{rname}' in request {idx} cannot be negative")

            total_demand[rname] = total_demand.get(rname, 0.0) + float(amount)

    # Feasibility check (missing resource => 0 capacity)
    for rname, demand in total_demand.items():
        cap = float(resources.get(rname, 0.0))
        if demand > cap:
            return False

    return True
