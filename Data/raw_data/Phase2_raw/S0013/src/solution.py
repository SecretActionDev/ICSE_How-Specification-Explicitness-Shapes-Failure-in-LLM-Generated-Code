from typing import Dict, List, Union
from collections import Counter

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.

    New requirement: At least one unit of some resource must remain unallocated after assignment.

    Args:
        resources : Dict[str, Number]
            Mapping from resource name to total available capacity.
        requests : List[Dict[str, Number]]
            List of requests. Each request is a mapping from resource name to the amount required.

    Returns:
        bool
            True if the allocation is feasible and at least one unit of some resource remains unallocated,
            False otherwise.
    """
    
    # Sum up total requests for each resource
    total_requests: Counter[str] = Counter()
    for req in requests:
        if not isinstance(req, dict):
            raise ValueError(f"Expected dict in requests, got {type(req)}: {req}")
        for res, count in req.items():
            total_requests[res] += count

    # Check if any request exceeds resource capacity
    for res, total in total_requests.items():
        if total > resources.get(res, 0):
            return False  # infeasible

    # Check new requirement: at least one resource must remain unallocated
    for res, capacity in resources.items():
        used = total_requests.get(res, 0)
        if used < capacity:
            return True  # feasible, some resource has leftover
    return False  # all resources fully consumed