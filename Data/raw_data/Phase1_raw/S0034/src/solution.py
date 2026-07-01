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
    # Validate that all requests are dictionaries
    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")
    
    # Calculate total demand for each resource
    total_demand = {}
    
    for request in requests:
        for resource, amount in request.items():
            # Check if the requested resource exists in available resources
            if resource not in resources:
                return False
            
            # Sum up the total demand for this resource
            total_demand[resource] = total_demand.get(resource, 0) + amount
    
    # Check if total demand for each resource exceeds available capacity
    for resource, capacity in resources.items():
        if total_demand.get(resource, 0) > capacity:
            return False
    
    return True