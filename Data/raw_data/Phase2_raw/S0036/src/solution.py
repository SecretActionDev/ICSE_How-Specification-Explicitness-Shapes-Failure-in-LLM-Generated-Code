from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.
    
    Raises:
        TypeError: If input types are incorrect.
        ValueError: If numeric values are invalid (negative, NaN, infinite) or structure invalid.
    
    Returns:
        bool: True if allocation is feasible and leaves at least 1 unit of every resource unallocated, False otherwise.
    """
    
    # Type validations
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")
    if resources is None or requests is None:
        raise TypeError("Resources and requests cannot be None")
    if len(resources) == 0:
        raise ValueError("Resources cannot be empty")
    
    # Check resource keys and values
    for r_key, r_val in resources.items():
        if not isinstance(r_key, str):
            raise TypeError("Resource keys must be strings")
        if not isinstance(r_val, (int, float)):
            raise TypeError("Resource values must be numbers")
        if r_val < 0 or math.isnan(r_val) or math.isinf(r_val):
            raise ValueError("Resource values must be non-negative finite numbers")
    
    # Initialize usage tracker
    total_used = {resource: 0 for resource in resources}
    
    # Process requests
    for i, request in enumerate(requests):
        if not isinstance(request, dict):
            raise TypeError(f"Request at index {i} must be a dictionary")
        for req_key, req_val in request.items():
            if not isinstance(req_key, str):
                raise TypeError("Request keys must be strings")
            if not isinstance(req_val, (int, float)):
                raise TypeError("Request values must be numbers")
            if isinstance(req_val, bool):
                raise TypeError("Request values must be numbers, not bool")
            if req_val < 0 or math.isnan(req_val) or math.isinf(req_val):
                raise ValueError("Request values must be non-negative finite numbers")
            if req_key not in resources:
                raise ValueError(f"Request resource '{req_key}' not defined in resources")
            if isinstance(req_val, dict):
                raise TypeError("Nested request values are not allowed")
            
            total_used[req_key] += req_val
            if total_used[req_key] > resources[req_key]:
                return False  # exceeds available capacity
    
    # Check at least 1 unit remains
    for resource, used in total_used.items():
        if resources[resource] - used < 1:
            return False
    
    return True