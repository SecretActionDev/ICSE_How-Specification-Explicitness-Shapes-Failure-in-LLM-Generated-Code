""" Stub file for the is allocation feasible exercise.
Implement the function is_allocation_feasible to determine whether
a set of resource requests can be satisfied given limited capacities.
"""

from typing import Dict, List, Union

Number = Union[int, float]


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied
    given limited capacities.

    Args:
        resources : Dict[str, Number]
            Mapping from resource name to total available capacity.
        requests : List[Dict[str, Number]]
            List of requests. Each request is a mapping from resource
            name to the amount required.

    Returns:
        True if the allocation is feasible, False otherwise.
    """

    # Validate resource capacities
    for resource, capacity in resources.items():
        if not isinstance(capacity, (int, float)):
            return False
        if capacity < 0:
            return False

    # Track total requested per resource
    total_requested: Dict[str, Number] = {r: 0 for r in resources}

    for request in requests:
        for resource, amount in request.items():

            # Resource must exist
            if resource not in resources:
                return False

            # Validate request amount
            if not isinstance(amount, (int, float)):
                return False
            if amount < 0:
                return False

            total_requested[resource] += amount

            # Early exit if exceeded
            if total_requested[resource] > resources[resource]:
                return False

    return True