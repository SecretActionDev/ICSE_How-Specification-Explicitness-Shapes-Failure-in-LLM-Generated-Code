## Student Name:Rajendra Brahmbhatt 
## Student ID: 217925157

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

    # TODO: Implement this function


    # Defensive check: capacities must be non-negative
    for capacity in resources.values():
        if capacity < 0:
            return False

    # Track total usage per resource
    usage: Dict[str, Number] = {}

    for request in requests:
        # Validate that each request is a dictionary
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")
        for resource, amount in request.items():
            # Requested amount must be non-negative
            if amount < 0:
                return False

            # Resource must exist
            if resource not in resources:
                return False

            # Accumulate usage
            usage[resource] = usage.get(resource, 0) + amount

            # Early exit if capacity exceeded
            if usage[resource] > resources[resource]:
                return False

    return True
