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
    """

    # Structural validation: resources must be a dict
    if not isinstance(resources, dict):
        raise ValueError("Resources must be a dictionary")

    total_requested: Dict[str, Number] = {}

    for request in requests:
        # Structural validation: each request must be a dict
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")

        for resource, amount in request.items():
            if resource not in resources:
                return False

            total_requested[resource] = total_requested.get(resource, 0) + amount

            if total_requested[resource] > resources[resource]:
                return False

    return True