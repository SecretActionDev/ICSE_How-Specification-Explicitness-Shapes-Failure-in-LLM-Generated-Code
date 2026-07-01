# Name: Mohsen Maoodhah
# Student Number: 220153425

from typing import Dict, List, Union

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determines whether a set of resource requests can be satisfied given limited capacity.

    Args:
        resources: Dictionary mapping resource names to available amounts.
        requests: List of dictionaries representing requested amounts for each resource.

    Returns:
        True if all requests can be satisfied without exceeding capacity and 
        at least one resource remains partially unallocated, False otherwise.

    Raises:
        ValueError: If `resources` is not a dictionary or if any request is invalid.
    """
    # Validate resources input
    if not isinstance(resources, dict):
        raise ValueError("The resources must be a dictionary")

    # Initialize total usage of each resource
    total_usage: Dict[str, Number] = {key: 0 for key in resources}

    # Aggregate requests
    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dict")

        for name, amount in request.items():
            if name not in resources:
                # Requested resource does not exist
                return False
            if not isinstance(amount, (int, float)):
                raise ValueError("Requested amount must be a number")
            total_usage[name] += amount

    # Check that requests do not exceed capacity
    for name, used in total_usage.items():
        if used > resources[name]:
            return False

    # Ensure at least one resource has leftover capacity
    has_leftover = any((resources[name] - used) > 0 for name, used in total_usage.items())
    if not has_leftover:
        return False

    return True