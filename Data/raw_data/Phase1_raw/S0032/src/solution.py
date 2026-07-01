## Student Name: Triya Augustine
## Student ID: 218859157

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

    used: Dict[str, Number] = {}

    for resource in resources:
        used[resource] = 0

    for request in requests:
        # NEW: structural validation
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")

        for resource, amount in request.items():
            if resource not in resources:
                return False

            if amount < 0:
                return False

            used[resource] += amount

            if used[resource] > resources[resource]:
                return False

    return True