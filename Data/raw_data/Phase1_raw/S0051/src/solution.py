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
    # Copy resources to track remaining capacity
    remaining = resources.copy()
    for request in requests:
        # Validate that each request is a dict
        if not isinstance(request, dict):
            raise ValueError(f"Each request must be a dictionary, got {type(request).__name__}")

        for resource, amount in request.items():
            # If resource is unknown, allocation is not feasible
            if resource not in remaining:
                return False
            # If request exceeds available, allocation is not feasible
            if amount > remaining[resource]:
                return False
            # Reduce remaining capacity
            remaining[resource] -= amount

    return True