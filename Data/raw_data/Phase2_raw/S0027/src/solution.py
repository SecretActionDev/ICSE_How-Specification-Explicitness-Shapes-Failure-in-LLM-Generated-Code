from typing import Dict, List, Union, Tuple

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> Tuple[bool, Dict[str, Number]]:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities,
    ensuring at least one resource remains unallocated for emergency or burst usage.

    Args:
        resources: Dict[str, Number] - Mapping from resource name to total available capacity.
        requests: List[Dict[str, Number]] - Each request is a mapping from resource name to the amount required.

    Returns:
        Tuple[bool, Dict[str, Number]] - 
            - True if the allocation is feasible and at least one resource remains.
            - False otherwise.
            - Dictionary of remaining resources after allocation attempt.
    """
    # Step 1: Validate requests
    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")

    # Step 2: Sum total demand per resource
    total_demand: Dict[str, Number] = {}
    for request in requests:
        for resource_name, amount in request.items():
            if amount < 0:
                raise ValueError("Resource requests must be non-negative")
            total_demand[resource_name] = total_demand.get(resource_name, 0) + amount

    # Step 3: Check feasibility and calculate remaining resources
    remaining_resources = resources.copy()
    for resource_name, demand in total_demand.items():
        if resource_name not in resources:
            return False, resources  # requested resource doesn't exist
        if demand > resources[resource_name]:
            return False, resources  # demand exceeds capacity
        remaining_resources[resource_name] -= demand

    # Step 4: Enforce new requirement - at least one resource must remain
    if all(amount <= 0 for amount in remaining_resources.values()):
        return False, remaining_resources

    return True, remaining_resources