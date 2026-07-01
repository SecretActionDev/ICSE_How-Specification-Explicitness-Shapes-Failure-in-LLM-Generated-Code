from typing import Dict, List, Union

Number = Union[int, float]


def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied given limited capacities.
    
    New requirement:
    At least one resource must remain unallocated after assignment.
    """

    # Error checking
    if not isinstance(resources, dict):
        raise ValueError("Undefined Resource!")

    for req in requests:
        if not isinstance(req, dict):
            raise ValueError("Not a Dictionary!")

    total_demand: Dict[str, float] = {}

    # Calculate total demand
    for i, req in enumerate(requests, 1):
        for res_name, amount in req.items():
            if res_name not in resources:
                return False
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                raise ValueError(
                    f"Invalid numeric value for resource '{res_name}' "
                    f"in request #{i}: {amount!r}"
                )
            if amount < 0:
                raise ValueError(
                    f"Negative value not allowed for resource '{res_name}' "
                    f"in request #{i}: {amount}"
                )

            total_demand[res_name] = total_demand.get(res_name, 0.0) + amount

    # Check feasibility AND track leftover
    has_leftover = False

    for res_name, available in resources.items():
        available = float(available)
        demanded = total_demand.get(res_name, 0.0)

        if demanded > available:
            return False

        if demanded < available:
            has_leftover = True

    # New requirement: at least one resource must remain unused
    return has_leftover