from typing import Dict, List, Union, Any

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    # Initialize total demand per resource type
    total_request = {r: 0 for r in resources}
    
    # Aggregate all requests
    for req in requests:
        for r_type, amount in req.items():
            if r_type not in resources:
                # Resource type mismatch
                return False
            if amount < 0:
                # Negative request not allowed
                return False
            total_request[r_type] += amount
    
    # Check if total request exceeds available resources
    for r_type, total in total_request.items():
        if total > resources[r_type]:
            return False
    
    return True