## Student Name: Elim Lemango
## Student ID: 216689424

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to  Determine whether a set of resource requests can be satisfied 
given limited capacities. Take int account any possible constraints. See the lab handout
for full requirements.
"""
    
from typing import Dict, List, Union

Number = Union[int, float]


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
# ---- Structural validation ----
    if not isinstance(resources, dict):
        raise ValueError("resources must be a dictionary")

    if not isinstance(requests, list):
        raise ValueError("requests must be a list")

    # ---- Validate resource capacities ----
    for resource, capacity in resources.items():
        if not isinstance(capacity, (int, float)):
            raise ValueError("resource capacities must be numeric")
        if capacity < 0:
            raise ValueError("resource capacities must be non-negative")

    total_allocated: Dict[str, Number] = {r: 0 for r in resources}

    # ---- Process requests ----
    for request in requests:

        if not isinstance(request, dict):
            raise ValueError("each request must be a dictionary")

        for resource, amount in request.items():

            if resource not in resources:
                return False

            if not isinstance(amount, (int, float)):
                raise ValueError("request amounts must be numeric")

            if amount < 0:
                raise ValueError("request amounts must be non-negative")

            total_allocated[resource] += amount

            if total_allocated[resource] > resources[resource]:
                return False

    # ---- NEW REQUIREMENT ----
    # At least one resource must remain unallocated
    at_least_one_remaining = any(
        total_allocated[r] < resources[r]
        for r in resources
    )

    return at_least_one_remaining