## Student Name: Richard Balroop
## Student ID: 216906349

"""
Stub file for the is allocation feasible exercise.

Implement the function `is_allocation_feasible` to  Determine whether a set of resource requests can be satisfied 
given limited capacities. Take int account any possible constraints. See the lab handout
for full requirements.
"""
    
from typing import Dict, List, Union

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
    flag = True
    for i in range(len(requests)):
        if requests[i] is None or not isinstance(requests[i], dict):
            flag = False
            break
        if not confirm_type_of_key_and_value(requests[i], str, Number):
            flag = False
            raise ValueError("Invalid type in requests list at index {}".format(i))
            break
    if not confirm_type_of_key_and_value(resources, str, Number):
        flag = False
        raise ValueError("Invalid type in resources dictionary")
    
    if flag:
        total_requests = build_total_request(requests)
        for key in total_requests:
            if key not in resources or total_requests[key] > resources[key]:
                flag = False
    
    return flag
            
    
    
    # TODO: Implement this function
    # raise NotImplementedError("suggest_slots function has not been implemented yet")

def confirm_type_of_key_and_value(dictionary, expected_key_type, expected_value_type):
    flag = True
    for key in dictionary:
        if not isinstance(key, expected_key_type) or not isinstance(dictionary[key], expected_value_type):
            flag = False
    return flag
    
def build_total_request(requests):
    total_requests = {}
    for request in requests:
        for key in request:
            if key in total_requests:
                total_requests[key] += request[key]
            else:
                total_requests[key] = request[key]
    return total_requests