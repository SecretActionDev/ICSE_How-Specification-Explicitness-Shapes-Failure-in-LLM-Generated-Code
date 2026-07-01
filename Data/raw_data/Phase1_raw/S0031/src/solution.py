from typing import Dict, List, Union
import math

Number = Union[int, float]


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:

    # Validate resources
    if not isinstance(resources, dict):
        raise ValueError("Resources must be a dictionary")

    for name, cap in resources.items():
        if not isinstance(cap, (int, float)):
            raise ValueError("Invalid capacity type")

        if math.isnan(cap) or math.isinf(cap) or cap < 0:
            raise ValueError("Invalid capacity value")

    # Track usage
    usage = {r: 0 for r in resources}

    # Process requests
    for req in requests:

        # Must be a dict
        if not isinstance(req, dict):
            raise ValueError("Each request must be a dictionary")

        for r, amount in req.items():

            # Unknown resource → infeasible (False, not exception)
            if r not in resources:
                return False

            # Must be numeric
            if not isinstance(amount, (int, float)):
                raise ValueError("Invalid request amount type")

            # Must be valid number
            if math.isnan(amount) or math.isinf(amount) or amount < 0:
                raise ValueError("Invalid request amount value")

            usage[r] += amount

            # Over capacity → infeasible
            if usage[r] > resources[r]:
                return False

    return True