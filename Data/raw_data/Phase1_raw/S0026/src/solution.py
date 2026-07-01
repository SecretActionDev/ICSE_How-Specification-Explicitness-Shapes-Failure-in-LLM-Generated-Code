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

    Raises:
        ValueError: If any request is not a dictionary.

    """
    # TODO: Implement this function
    # Validate that all requests are dictionaries
    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("All requests must be dictionaries")
    
    # Calculate total demand for each resource
    total_demand = {}
    for request in requests:
        for resource_name, amount in request.items():
            # Check if the resource exists in available resources
            if resource_name not in resources:
                return False
            
            # Accumulate the demand for this resource
            if resource_name in total_demand:
                total_demand[resource_name] += amount
            else:
                total_demand[resource_name] = amount
    
    # Check if total demand exceeds capacity for any resource
    for resource_name, capacity in resources.items():
        demand = total_demand.get(resource_name, 0)
        if demand > capacity:
            return False
    
    # All constraints satisfied
    return True