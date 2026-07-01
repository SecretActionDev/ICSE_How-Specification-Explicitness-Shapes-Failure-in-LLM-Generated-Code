from typing import Dict, List, Union
import math

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    # ----------------------
    # TYPE VALIDATION
    # ----------------------
    if resources is None:
        raise TypeError("Resources cannot be None.")
    if requests is None:
        raise TypeError("Requests cannot be None.")
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary.")
    if not isinstance(requests, list):
        raise TypeError("Requests must be provided as a list of dictionaries.")
    if len(resources) == 0:
        raise ValueError("Resources dictionary cannot be empty.")

    for r_key, r_val in resources.items():
        if not isinstance(r_key, str):
            raise TypeError("Resource keys must be strings.")
        if not isinstance(r_val, (int, float)):
            raise TypeError("Resource values must be numbers.")
        if isinstance(r_val, bool):
            raise TypeError("Resource values must be numbers, not boolean.")
        if math.isnan(r_val) or math.isinf(r_val) or r_val < 0:
            raise ValueError("Resource values must be non-negative finite numbers.")

    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("Each request must be a dictionary.")
        for req_key, req_val in req.items():
            if not isinstance(req_key, str):
                raise TypeError("Request keys must be strings.")
            if req_key not in resources:
                raise ValueError(f"Request key '{req_key}' not defined in resources.")
            if not isinstance(req_val, (int, float)):
                raise TypeError("Request values must be numbers.")
            if isinstance(req_val, bool):
                raise TypeError("Request values must be numbers, not boolean.")
            if math.isnan(req_val) or math.isinf(req_val) or req_val < 0:
                raise ValueError("Request values must be non-negative finite numbers.")
            if isinstance(req_val, (list, tuple, dict)):
                raise TypeError("Request values must be scalar numbers, not nested structures.")

    # ----------------------
    # AGGREGATE REQUESTS
    # ----------------------
    total_requested = {res: 0 for res in resources}

    for req in requests:
        for key, val in req.items():
            total_requested[key] += val

    # ----------------------
    # CHECK FEASIBILITY
    # ----------------------
    all_fully_consumed = True

    for res, total in total_requested.items():
        if total > resources[res]:
            return False  # cannot satisfy this request
        if total < resources[res]:
            all_fully_consumed = False  # at least one unit remains

    # Must leave at least one resource unallocated
    if all_fully_consumed:
        return False

    return True