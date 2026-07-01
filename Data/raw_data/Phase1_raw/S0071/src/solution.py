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
    if not isinstance(resources, dict):
        raise TypeError("Resources must be a dictionary.")
    if not isinstance(requests, list):
        raise TypeError("Requests must be provided as a list of dictionaries.")
    if resources is None:
        raise TypeError("Resources cannot be None.")
    if requests is None:
        raise TypeError("Requests cannot be None.")
    if len(resources) == 0:
        raise ValueError("Resources dictionary cannot be empty.")

    for r_key, r_val in resources.items():
        if not isinstance(r_key, str):
            raise TypeError("Resource keys must be strings.")
        if not isinstance(r_val, (int, float)):
            raise TypeError("Resource values must be numbers.")
        if math.isnan(r_val) or math.isinf(r_val) or r_val < 0:
            raise ValueError("Resource values must be non-negative finite numbers.")

    for req in requests:
        if not isinstance(req, dict):
            raise TypeError("Each request must be a dictionary.")
        for req_key, req_val in req.items():
            if not isinstance(req_key, str):
                raise TypeError("Request keys must be strings.")
            if not isinstance(req_val, (int, float)):
                raise TypeError("Request values must be numbers.")
            if isinstance(req_val, bool):  # prevent True/False passing as int
                raise TypeError("Request values must be numbers, not boolean.")
            if math.isnan(req_val) or math.isinf(req_val) or req_val < 0:
                raise ValueError("Request values must be non-negative finite numbers.")
            if req_key not in resources:
                raise ValueError(f"Request key '{req_key}' not defined in resources.")

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
    for res, total in total_requested.items():
        if total > resources[res]:
            return False

    return True