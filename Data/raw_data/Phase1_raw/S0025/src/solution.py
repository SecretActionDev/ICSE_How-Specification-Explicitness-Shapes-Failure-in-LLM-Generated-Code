##Student Name: Negar Khalilazar
##Student ID: 221037437
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
    total_demand: Dict[str, Number] = {name: 0 for name in resources}
    for req in requests:
        for r_name, amount in req.items():
            if r_name not in resources or amount < 0:
                return False
            total_demand[r_name] += amount
        for r_name, capacity in resources.items():
            if total_demand[r_name] > capacity:
                return False
        return True
    raise NotImplementedError("suggest_slots function has not been implemented yet")
