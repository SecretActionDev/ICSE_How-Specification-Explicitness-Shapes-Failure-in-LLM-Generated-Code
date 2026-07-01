## Student Name: Vikram Singh Chauhan
## Student ID: 220914867

import pytest
# Ensure this matches your folder structure (e.g. 'from src.solution' or 'from solution')
from src.solution import is_allocation_feasible

# ORIGINAL TESTS 

def test_basic_feasible_single_resource():
    # Basic Feasible Single-Resource
    # Demand (9) < Capacity (10) -> Feasible
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 2}]
    assert is_allocation_feasible(resources, requests) is True

def test_multi_resource_infeasible_one_overloaded():
    # Multi-Resource Infeasible (one overload)
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False

def test_missing_resource_in_availability():
    # Missing Resource in Requests
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_non_dict_request_raises():
    # Non-Dict Request Raises Error
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]  # Malformed request
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

# NEW TESTS FOR NEW REQUIREMENT 

def test_exact_capacity_match_fails():
    # NEW REQUIREMENT: "An allocation that consumes all available resources is no longer valid."
    # Scenario: Demand exactly equals capacity for ALL resources.
    resources = {'cpu': 10, 'mem': 16}
    requests = [{'cpu': 5, 'mem': 8}, {'cpu': 5, 'mem': 8}]
    # Total used: CPU 10/10, MEM 16/16. No spare capacity.
    assert is_allocation_feasible(resources, requests) is False

def test_full_utilization_with_one_spare():
    # NEW REQUIREMENT CLARIFICATION
    # Scenario: One resource is full (100%), but another has spare room.
    # This should PASS because "at least one resource" remains unallocated.
    resources = {'cpu': 10, 'mem': 20}
    requests = [{'cpu': 10, 'mem': 15}]
    # CPU: 10/10 (0 spare), MEM: 15/20 (5 spare).
    assert is_allocation_feasible(resources, requests) is True

def test_empty_requests_always_feasible():
    # Empty requests = 0 demand = 100% spare capacity.
    resources = {'cpu': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_floating_point_resources():
    # Floating Point Precision check
    resources = {'bandwidth': 10.5}
    requests = [{'bandwidth': 5.0}, {'bandwidth': 4.0}] 
    # Total 9.0 / 10.5 -> Has spare capacity.
    assert is_allocation_feasible(resources, requests) is True

def test_zero_capacity_resource():
    # Zero Capacity Resource
    # Even if demand is 0, if capacity is 0, do we have spare capacity? 
    # 0 < 0 is False. So if capacity is 0, we can never have "unallocated" resources.
    resources = {'cpu': 0}
    requests = [] # 0 demand
    # 0 demand == 0 capacity. No spare room. Should fail based on strict reading of "remain unallocated".
    assert is_allocation_feasible(resources, requests) is False
