from typing import Dict, List, Union
from collections import defaultdict

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.

    Rules:
    - If a request references a resource not in `resources`, its capacity is treated as 0
      and the allocation fails (returns False).
    - Negative request amounts are not allowed.
    - Requests are indivisible.
    - Request order does not matter.
    - At least one resource must remain unallocated after assignment.
    """

    # Validate resource capacities
    for r, cap in resources.items():
        if cap < 0:
            raise ValueError(f"Resource capacity for '{r}' must be non-negative")

    total_demand: Dict[str, Number] = defaultdict(float)

    # Sum up all requests per resource
    for i, request in enumerate(requests):
        if not isinstance(request, dict):
            raise ValueError(f"Request at index {i} must be a dictionary")

        for resource, amount in request.items():
            if not isinstance(amount, (int, float)):
                raise ValueError(
                    f"Non-numeric request amount for resource '{resource}' in request index {i}"
                )

            if amount < 0:
                raise ValueError(
                    f"Negative request amount for resource '{resource}' in request index {i}"
                )

            if resource not in resources:
                return False  # Requested resource does not exist

            total_demand[resource] += amount

    # Check if total demand exceeds capacities
    for resource, demand in total_demand.items():
        if demand > resources[resource]:
            return False

    # Check the new requirement: at least one resource must remain unallocated
    for resource, capacity in resources.items():
        remaining = capacity - total_demand.get(resource, 0)
        if remaining > 0:
            return True  # At least one resource has leftover capacity

    # All resources are fully consumed _ invalid allocation
    return False