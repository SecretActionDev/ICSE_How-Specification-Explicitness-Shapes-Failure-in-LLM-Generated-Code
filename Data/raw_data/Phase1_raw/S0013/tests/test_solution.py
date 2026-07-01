## Student Name: James Prime
## Student ID: 215028657

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
    assert is_allocation_feasible(resources, requests) is True

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

# Requirement — Infeasible when over‑requested
# Description: If a total requested amount for any resource exceeds what is available, the function must return

def test_over_request_false():
    resources = {"cpu": 8, "mem": 16}
    requests = [
        {"cpu": 5},
        {"cpu": 5},  # Total CPU = 10 > 8
    ]
    assert is_allocation_feasible(resources, requests) is False

# Missing resource treated as zero
# Description: If the request includes a resource that is not present in the resources map, 
# treat availability as 0 and return False if requested. For example, requesting "disk" when resources contain no "disk".

def test_missing_resource():
    resources = {"cpu": 4}
    requests = [
        {"cpu": 2},
        {"disk": 10}  # Resource "disk" not in resources
    ]
    assert is_allocation_feasible(resources, requests) is False

#Zero requests are always feasible
# Description: If all request counts sum to zero, or the request list is empty, the function should return True

def test_zero_or_empty_requests():
    resources = {"cpu": 4, "mem": 8}
    requests = []  # no requests
    assert is_allocation_feasible(resources, requests) is True

#Requirement — Multiple resources aggregated independently
#Description: Each resource type should be considered independently (e.g., sum of CPUs is separate from sum of memory). 
#The function should return True if all resource requests are feasible individually.

def test_independent_resource_sums():
    resources = {"cpu": 6, "mem": 10}
    requests = [
        {"cpu": 2, "mem": 4},
        {"cpu": 3, "mem": 6},
    ]
    # CPU total = 5 <= 6, mem total = 10 <= 10
    assert is_allocation_feasible(resources, requests) is True

#Boundary/Edge case request equal to resource

#Description: If a requested resource exactly equals the available quantity for that resource, the allocation should be considered feasible (True). 
#This covers an edge case where request totals hit the exact resource limit — a classic area to test per testing textbooks (e.g., boundary value analysis).
def test_request_equal_to_resource():
    resources = {"cpu": 5, "mem": 10}
    requests = [
        {"cpu": 2},
        {"cpu": 3},  # total cpu = 5, exactly available
        {"mem": 10}, # total mem = 10, exactly available
    ]
    assert is_allocation_feasible(resources, requests) is True
