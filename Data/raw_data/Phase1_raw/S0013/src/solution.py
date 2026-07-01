## Student Name: James Prime
## Student ID: 215028657

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to  Determine whether a set of resource requests can be satisfied 
given limited capacities. Take int account any possible constraints. See the lab handout
for full requirements.
"""
    
from typing import Dict, List, Union
from collections import Counter

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
    
    # make count
    total_requests: Counter[str] = Counter()

    for req in requests:
        if not isinstance(req, dict):
            raise ValueError(f"Expected dict in requests, got {type(req)}: {req}")
        for res, count in req.items():
            total_requests[res] += count

    # check count, if total is more for that resource return false
    for res, total in total_requests.items():
        if total > resources.get(res, 0):
            return False

    return True
    