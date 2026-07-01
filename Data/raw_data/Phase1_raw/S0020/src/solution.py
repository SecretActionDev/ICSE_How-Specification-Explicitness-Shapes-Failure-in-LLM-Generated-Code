# Name: Mohsen Maoodhah
# Student Number: 220153425

from typing import Dict, List, Union

Number = Union[int, float]


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    # Checking if resources is a dictionary
    if not isinstance(resources, dict):
        raise ValueError("The resources must be a dictionary")

    # Maps each resource to the total usage. Initializes each resource in resources to 0.
    total_usage: Dict[str, Number] = {key: 0 for key in resources}

    # Going through the list of dictionaries to calculate the total sum for each resource
    for request in requests:
        # Making sure a request is a dictionary
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dict")

        for name, amount in request.items():
            if name not in resources:
                return False
            if not isinstance(amount, (int, float)):
                raise ValueError("Requested amount must be a number")

            total_usage[name] += amount

    # Old rule: cannot exceed capacity
    for name, used in total_usage.items():
        if used > resources[name]:
            return False

    # New rule: at least one resource must remain unallocated (strictly positive leftover)
    # i.e., allocation is invalid if it consumes ALL available resources exactly.
    has_leftover = any((resources[name] - used) > 0 for name, used in total_usage.items())
    if not has_leftover:
        return False

    return True
