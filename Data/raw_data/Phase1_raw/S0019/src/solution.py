## Student Name: Mohammad Mustafidur Rahman
## Student ID: 220081014

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

    total_demand = {}

    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("All the request have to be a dictionary")
        
        for resource_name, amount in request.items():
            if resource_name not in resources:
                return False
            
            total_demand[resource_name] = total_demand.get(resource_name, 0) + amount

    for resource_name, demand_amount in total_demand.items():
        if demand_amount > resources[resource_name]:
            return False
    return True  
    
    ## TODO: Implement this function
