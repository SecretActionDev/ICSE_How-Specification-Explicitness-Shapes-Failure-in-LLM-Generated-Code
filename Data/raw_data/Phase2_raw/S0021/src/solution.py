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

    Additional requirement:
    At least one resource must remain unallocated after assignment.
    An allocation that consumes all available resources is not valid.

    Raises:
        ValueError if the inputs are structurally invalid.
    """

    # Validate resources structure
    if not isinstance(resources, dict):
        raise ValueError("resources must be a dictionary")

    for rname, cap in resources.items():
        if not isinstance(rname, str):
            raise ValueError("resource names must be strings")
        if not isinstance(cap, (int, float)):
            raise ValueError("resource capacity must be numeric")
        if cap < 0:
            raise ValueError("resource capacity cannot be negative")

    # Validate requests structure
    if not isinstance(requests, list):
        raise ValueError("requests must be a list")

    total_demand: Dict[str, float] = {}

    for i, req in enumerate(requests):
        if not isinstance(req, dict):
            raise ValueError("each request must be a dictionary")

        for rname, amount in req.items():
            if not isinstance(rname, str):
                raise ValueError("resource names in requests must be strings")
            if not isinstance(amount, (int, float)):
                raise ValueError("request amounts must be numeric")
            if amount < 0:
                raise ValueError("request amounts cannot be negative")

            total_demand[rname] = total_demand.get(rname, 0) + amount

    # Check capacity constraints
    for rname, demand in total_demand.items():
        capacity = resources.get(rname, 0)
        if demand > capacity:
            return False

    # New requirement: at least one resource must remain unused
    for rname, capacity in resources.items():
        demand = total_demand.get(rname, 0)
        if capacity - demand > 0:
            return True

    return False
