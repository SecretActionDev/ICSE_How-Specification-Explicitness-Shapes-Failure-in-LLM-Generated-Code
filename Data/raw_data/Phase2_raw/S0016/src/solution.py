from typing import Dict, List, Union

Number = Union[int, float]


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities,
    ensuring at least one unit of some resource remains unallocated.

    Args:
        resources : Dict[str, Number]
            Mapping from resource name to total available capacity.
        requests : List[Dict[str, Number]]
            List of requests. Each request is a mapping from resource name to the amount required.

    Returns:
        True if the allocation is feasible AND leaves at least one resource partially unused, False otherwise.
    """
    available = resources.copy()
    
    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary.")
        for resource, amount in request.items():
            if resource not in available:
                return False
            available[resource] -= amount
            if available[resource] < 0:
                return False

    # New requirement: at least one resource must remain unallocated
    if all(value == 0 for value in available.values()):
        return False
    
    return True