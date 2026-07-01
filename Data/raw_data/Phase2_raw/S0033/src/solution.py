from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities,
    ensuring at least one unit of some resource remains unallocated.
    
    Raises:
        TypeError: If input types are invalid.
        ValueError: If numeric values are invalid (negative, NaN, infinite) or requests contain unknown resources.

    Args:
        resources : Dict[str, Number], Mapping from resource name to total available capacity.
        requests : List[Dict[str, Number]], List of requests. Each request is a mapping from resource name to the amount required.

    Returns:
        True if the allocation is feasible and leaves at least one resource unallocated, False otherwise.
    """

    # --- Type checks ---
    if resources is None or not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if requests is None or not isinstance(requests, list):
        raise TypeError("Requests must be a list")
    if not resources:
        raise ValueError("Resources dictionary cannot be empty")

    # Validate resource keys and values
    for key, value in resources.items():
        if not isinstance(key, str):
            raise TypeError("Resource keys must be strings")
        if not isinstance(value, (int, float)):
            raise TypeError("Resource values must be numbers")
        if math.isnan(value) or math.isinf(value) or value < 0:
            raise ValueError("Resource values must be non-negative, finite numbers")

    usage: Dict[str, Number] = {}

    for request in requests:
        if not isinstance(request, dict):
            raise TypeError("Each request must be a dictionary")
        
        for key, value in request.items():
            # Key and value validation
            if not isinstance(key, str):
                raise TypeError("Request keys must be strings")
            if key not in resources:
                raise ValueError(f"Request contains unknown resource: {key}")
            if not isinstance(value, (int, float)):
                raise TypeError("Request values must be numbers")
            if math.isnan(value) or math.isinf(value) or value < 0:
                raise ValueError("Request values must be non-negative, finite numbers")
            if isinstance(value, dict) or isinstance(value, list):
                raise TypeError("Request values must be numeric, not nested structures")
            
            # Accumulate usage
            usage[key] = usage.get(key, 0) + value

            # Early exit if capacity exceeded
            if usage[key] > resources[key]:
                return False

    # Check that at least one resource remains unallocated
    for resource, total_capacity in resources.items():
        allocated = usage.get(resource, 0)
        if allocated < total_capacity:
            return True

    return False