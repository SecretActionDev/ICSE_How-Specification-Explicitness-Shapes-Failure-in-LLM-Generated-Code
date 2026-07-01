## Student Name: Cyrus Yang
## Student ID: 219583038

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to  Determine whether a set of resource requests can be satisfied 
given limited capacities. Take int account any possible constraints. See the lab handout
for full requirements.
"""
    
from typing import Dict, List, Union

from numpy.ma.core import empty

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
    total_demand = {}
    # Error Checking
    if not isinstance(resources, dict):
        raise ValueError("Undefined Resource!")
    for req in requests:
        if not isinstance(req, dict):
            raise ValueError("Not a Dictionary!")

    total_demand: Dict[str, float] = {}

    for i, req in enumerate(requests, 1):
        if not isinstance(req, dict):
            raise ValueError(f"Request is not a dictionary")
        for res_name, amount in req.items():
            if res_name not in resources:
                return False
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                raise ValueError(
                    f"Invalid numeric value for resource '{res_name}' "
                    f"in request #{i}: {amount!r}"
                )
            if amount < 0:
                raise ValueError(
                    f"Negative value not allowed for resource '{res_name}' "
                    f"in request #{i}: {amount}"
                )
            total_demand[res_name] = total_demand.get(res_name, 0.0) + amount

    for res_name, demanded in total_demand.items():
        available = float(resources[res_name])
        if demanded > available:
            return False

    return True