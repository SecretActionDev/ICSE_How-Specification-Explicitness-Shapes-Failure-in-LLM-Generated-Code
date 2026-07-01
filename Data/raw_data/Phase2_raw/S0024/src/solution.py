## Student Name:
## Student ID: 

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
    resources_copy = {k: v for k, v in resources.items()}
    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")
        for resource, amount in request.items():
            if resource not in resources:
                return False
            if not isinstance(amount, (int, float)) or amount < 0:
                raise ValueError("Resource amounts must be non-negative numbers")
            if amount > resources_copy[resource]:
                return False
            resources_copy[resource] -= amount
    return any(v > 0 for v in resources_copy.values())