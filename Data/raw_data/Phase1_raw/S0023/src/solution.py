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
    total_requested: Dict[str, Number] = {}

    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Request is not a dictionary.")
        
        for name, amount in request.items():
            if amount > 0:
                total_requested[name] = total_requested.get(name, 0) + amount

    for name, total_amount in total_requested.items():
        if name not in resources or total_amount > resources[name]:
            return False
    
    return True