from __future__ import annotations
from typing import Dict, List, Union
import math

Number = Union[int, float]


def _is_valid_number(x) -> bool:
    """True for int/float (not bool), finite, and not NaN."""
    if isinstance(x, bool):
        return False
    if not isinstance(x, (int, float)):
        return False
    return math.isfinite(x)


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.

    Interpretation:
    - Allocation is feasible iff, for every resource key in `resources`,
      the SUM of all request amounts for that resource <= capacity.
    - If any request references a resource not present in `resources`, infeasible (False).
    - Missing resource entries inside a request are treated as 0 (no demand).
    - A request value of None is treated as 0.
    - Negative capacities or negative demands are invalid -> ValueError.
    - Non-dict requests, non-dict resources, or non-numeric values -> ValueError.
    - NaN/Inf are invalid -> ValueError.
    - NEW REQUIREMENT:
        At least one resource must remain with unused capacity after allocation.
        If all resources are exactly fully utilized, return False.

    Returns:
        True if feasible, False otherwise.
    """
    if not isinstance(resources, dict):
        raise ValueError("resources must be a dict[str, number].")
    if not isinstance(requests, list):
        raise ValueError("requests must be a list[dict[str, number]].")

    # Validate resources
    for k, cap in resources.items():
        if not isinstance(k, str):
            raise ValueError("resource names must be strings.")
        if cap is None:
            raise ValueError(f"capacity for resource '{k}' cannot be None.")
        if not _is_valid_number(cap):
            raise ValueError(f"capacity for resource '{k}' must be a finite number.")
        if cap < 0:
            raise ValueError(f"capacity for resource '{k}' cannot be negative.")

    demand: Dict[str, float] = {k: 0.0 for k in resources.keys()}

    for idx, req in enumerate(requests):
        if not isinstance(req, dict):
            raise ValueError(f"request at index {idx} must be a dict[str, number].")

        for rname, amount in req.items():
            if not isinstance(rname, str):
                raise ValueError(f"resource name in request at index {idx} must be a string.")

            if rname not in resources:
                return False

            if amount is None:
                continue

            if not _is_valid_number(amount):
                raise ValueError(
                    f"amount for resource '{rname}' in request at index {idx} must be a finite number."
                )
            if amount < 0:
                raise ValueError(
                    f"amount for resource '{rname}' in request at index {idx} cannot be negative."
                )

            demand[rname] += float(amount)

            if demand[rname] > float(resources[rname]):
                return False

    # Ensure at least one resource remains unused
    for rname in resources:
        if demand[rname] < float(resources[rname]):
            return True  # at least one has remaining capacity

    return False  # all resources fully consumed → invalid under new rule