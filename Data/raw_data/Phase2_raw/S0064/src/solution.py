from typing import Dict, List
import numbers
import math

def is_allocation_feasible(
    resources: Dict[str, numbers.Number],
    requests: List[Dict[str, numbers.Number]]
) -> bool:
    """
    Determines if a set of resource requests can be allocated given available capacities,
    while ensuring at least one resource remains partially unallocated.

    Args:
        resources (Dict[str, numbers.Number]): Mapping of resource names to available capacities.
        requests (List[Dict[str, numbers.Number]]): List of requests, each a dict mapping
            resource names to requested amounts.

    Returns:
        bool: True if allocation is feasible and at least one resource remains partially unused.

    Raises:
        TypeError: If inputs are not of the expected types.
        ValueError: If any request references undefined resources, or resources/requests
            contain invalid numeric values.
    """

    # Validate top-level types
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary.")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list of dictionaries.")
    if resources is None:
        raise TypeError("Resources cannot be None.")
    if requests is None:
        raise TypeError("Requests cannot be None.")
    if not resources:
        raise ValueError("Resources dictionary cannot be empty.")

    # Validate resource names and capacities
    for res_name, capacity in resources.items():
        if not isinstance(res_name, str):
            raise TypeError("Resource names must be strings.")
        if not isinstance(capacity, numbers.Number) or isinstance(capacity, bool):
            raise TypeError("Resource capacities must be numeric (int/float).")
        if capacity < 0 or math.isnan(capacity) or math.isinf(capacity):
            raise ValueError("Resource capacities must be non-negative finite numbers.")

    # Initialize allocated totals
    total_allocated = {res_name: 0 for res_name in resources}

    # Validate and process each request
    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("Each request must be a dictionary.")

        for res_name, amount in req.items():
            # Validate keys
            if not isinstance(res_name, str):
                raise TypeError("Request keys must be strings.")
            if res_name not in resources:
                raise ValueError(f"Resource '{res_name}' not defined in resources.")

            # Validate amount
            if not isinstance(amount, numbers.Number) or isinstance(amount, bool):
                raise TypeError("Request values must be numeric (int/float).")
            if isinstance(amount, (list, tuple, dict)):
                raise TypeError("Request values must be numeric, not container types.")
            if amount < 0 or math.isnan(amount) or math.isinf(amount):
                raise ValueError("Request values must be non-negative finite numbers.")

            total_allocated[res_name] += amount
            if total_allocated[res_name] > resources[res_name]:
                return False  # exceeds capacity

    # Enforce "at least one resource must remain partially unallocated"
    any_unallocated = any(total_allocated[res] < resources[res] for res in resources)
    if not any_unallocated:
        return False

    return True