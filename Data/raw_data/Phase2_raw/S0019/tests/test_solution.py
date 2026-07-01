## Student Name: Mohammad Mustafidur Rahman
## Student ID: 220081014

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
from solution import is_allocation_feasible
import pytest


def test_basic_feasible_single_resource():
    # Basic Feasible Single-Resource
    # Constraint: total demand <= capacity
    # Reason: check basic functional requirement
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 3}]
    ## UPDATE: Changed expectation to False. 
    # The new requirement mandates at least one unallocated resource. 
    # Since 3+4+3=10 (100% capacity), this allocation is now invalid.
    assert is_allocation_feasible(resources, requests) is False

def test_multi_resource_infeasible_one_overloaded():
    # Multi-Resource Infeasible (one overload)
    # Constraint: one resource exceeds capacity
    # Reason: check detection of per-resource infeasibility
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False

def test_missing_resource_in_availability():
    # Missing Resource in Requests
    # Constraint: request references unavailable resource
    # Reason: allocation must be infeasible
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_non_dict_request_raises():
    # Non-Dict Request Raises Error
    # Constraint: structural validation
    # Reason: request must be a dict
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]  # malformed request
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

"""TODO: Add at least 5 additional test cases to test your implementation."""
def test_empty_requests_list():
    #Zero demand should always be feasible.
    resources = {'cpu': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_exact_capacity_boundary():
    # Testing the edge case (New Requirement Test).
    # 10/10 CPU used, 50/50 Mem used.
    # PREVIOUSLY: True. NOW: False (must leave at least one unallocated).
    resources = {'cpu': 10, 'mem': 50}
    requests = [{'cpu': 10, 'mem': 25}, {'mem': 25}]
    assert is_allocation_feasible(resources, requests) is False

def test_floating_point_resources():
    # Ensure the function handles float capacities and demands correctly.
    # 0.7 + 0.8 = 1.5. Capacity is 1.5.
    # PREVIOUSLY: True. NOW: False (0 left over).
    resources = {'bandwidth': 1.5}
    requests = [{'bandwidth': 0.7}, {'bandwidth': 0.8}]
    assert is_allocation_feasible(resources, requests) is False

def test_zero_value_requests():
    # Requests for 0 units. Total used: 5. Capacity: 5.
    # PREVIOUSLY: True. NOW: False.
    resources = {'cpu': 5}
    requests = [{'cpu': 0}, {'cpu': 5}]
    assert is_allocation_feasible(resources, requests) is False

def test_large_number_feasibility():
    # For very large resource values.
    # Sum is exactly 10^12. Capacity is 10^12.
    # PREVIOUSLY: True. NOW: False.
    resources = {'storage': 10**12}
    requests = [{'storage': 5 * 10**11}, {'storage': 5 * 10**11}]
    assert is_allocation_feasible(resources, requests) is False

def test_new_requirement_strict_inequality():
    # NEW TEST: This check explicity under the capacity still correct.
    # Capacity 10. Requests 9. Leftover 1.
    resources = {'cpu': 10}
    requests = [{'cpu': 5}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is True
