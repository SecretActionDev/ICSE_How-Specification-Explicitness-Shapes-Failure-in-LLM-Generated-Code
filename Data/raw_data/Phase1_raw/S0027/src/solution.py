## Student Name:
## Student ID: 

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
    # Step 1: Validate that all requests are dictionaries
    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")
    
    # Step 2: Calculate total demand for each resource across all requests
    total_demand: Dict[str, Number] = {}
    
    for request in requests:
        for resource_name, amount in request.items():
            if resource_name in total_demand:
                total_demand[resource_name] += amount
            else:
                total_demand[resource_name] = amount
    
    # Step 3: Check if every resource demand can be satisfied
    for resource_name, demand in total_demand.items():
        # If a resource is requested but not available, allocation is infeasible
        if resource_name not in resources:
            return False
        
        # If demand exceeds available capacity, allocation is infeasible
        if demand > resources[resource_name]:
            return False
    
    # All checks passed - allocation is feasible
    return True