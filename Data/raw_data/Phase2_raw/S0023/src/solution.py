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
    Determine whether a set of resource requests can be satisfied given limited capacities,
    ensuring at least one resource remains partially or fully unallocated.

    Args:
        resources : Dict[str, Number], Mapping from resource name to total available capacity.
        requests : List[Dict[str, Number]], List of requests. Each request is a mapping from resource name to the amount required.

    Returns:
        True if the allocation is feasible AND leaves at least one unallocated resource, False otherwise.
    """
    # If the system has zero resources to begin with, nothing can remain unallocated
    if not resources:
        return False

    total_requested: Dict[str, Number] = {}

    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Request is not a dictionary.")
        
        for name, amount in request.items():
            if amount > 0:
                total_requested[name] = total_requested.get(name, 0) + amount

    # Check standard capacity constraints (can't ask for missing resources or exceed capacity)
    for name, total_amount in total_requested.items():
        if name not in resources or total_amount > resources[name]:
            return False

    # NEW REQUIREMENT: Ensure at least one resource is not completely consumed
    has_unallocated = False
    for name, capacity in resources.items():
        # If capacity is greater than what was requested (or if it wasn't requested at all, defaulting to 0)
        if capacity > total_requested.get(name, 0):
            has_unallocated = True
            break
            
    if not has_unallocated:
        return False
        
    return True