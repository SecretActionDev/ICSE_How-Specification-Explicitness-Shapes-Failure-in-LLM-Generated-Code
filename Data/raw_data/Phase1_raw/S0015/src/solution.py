## Student Name: Dexter Sargent
## Student ID: 217931460

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to  Determine whether a set of resource requests can be satisfied 
given limited capacities. Take int account any possible constraints. See the lab handout
for full requirements.
"""
    
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
      and a ValueError is raised.
    - Negative request amounts are not allowed.
    - Requests are indivisible.
    - Request order does not matter.
    """

    # Validate resource capacities
    for r, cap in resources.items():
        if cap < 0:
            raise ValueError(f"Resource capacity for '{r}' must be non-negative")

    total_demand: Dict[str, Number] = defaultdict(float)

    for i, request in enumerate(requests):
        if not isinstance(request, dict):
            raise ValueError(f"Request at index {i} must be a dictionary")

        for resource, amount in request.items():
            if not isinstance(amount, (int, float)):
                raise ValueError(
                    f"Non-numeric request amount for resource '{resource}' "
                    f"in request index {i}"
                )

            if amount < 0:
                raise ValueError(
                    f"Negative request amount for resource '{resource}' "
                    f"in request index {i}"
                )

            if resource not in resources:
                return False

            total_demand[resource] += amount

    for resource, demand in total_demand.items():
        if demand > resources[resource]:
            return False

    return True