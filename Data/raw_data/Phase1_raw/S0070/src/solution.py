from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    # --- Type checks ---
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary")
    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")
    
    if resources is None:
        raise TypeError("Resources cannot be None")
    if requests is None:
        raise TypeError("Requests cannot be None")
    
    if len(resources) == 0:
        if len(requests) == 0:
            raise ValueError("Empty resources with empty requests is invalid")
        raise ValueError("Resource dict cannot be empty")
    
    # --- Validate resources ---
    for k, v in resources.items():
        if not isinstance(k, str):
            raise TypeError(f"Resource key '{k}' must be a string")
        if isinstance(v, bool):
            raise TypeError(f"Resource value for '{k}' cannot be boolean")
        if not isinstance(v, (int, float)):
            raise TypeError(f"Resource value for '{k}' must be a number")
        if v < 0 or math.isnan(v) or math.isinf(v):
            raise ValueError(f"Resource value for '{k}' must be a non-negative finite number")
    
    # --- Validate requests ---
    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("Each request must be a dictionary")
        for k, v in req.items():
            if not isinstance(k, str):
                raise TypeError(f"Request key '{k}' must be a string")
            if k not in resources:
                raise ValueError(f"Request resource '{k}' is not valid")
            if isinstance(v, bool):
                raise TypeError(f"Request value for '{k}' cannot be boolean")
            if not isinstance(v, (int, float)):
                raise TypeError(f"Request value for '{k}' must be a number")
            if v < 0 or math.isnan(v) or math.isinf(v):
                raise ValueError(f"Request value for '{k}' must be non-negative finite number")
    
    # --- Allocation check ---
    remaining = resources.copy()
    for req in requests:
        # Check feasibility first
        for res, amt in req.items():
            if amt > remaining[res]:
                return False
        # Allocate
        for res, amt in req.items():
            remaining[res] -= amt
    
    return True