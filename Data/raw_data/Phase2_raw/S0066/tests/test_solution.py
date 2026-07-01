## Student Name:
## Student ID: 

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
def test_exact_capacity_match():
    # Exact Capacity Match
    # Constraint: total demand == capacity
    # Reason: boundary case should still be feasible
    resources = {'cpu': 10, 'mem': 20}
    requests = [{'cpu': 4, 'mem': 5}, {'cpu': 6, 'mem': 15}]
    assert is_allocation_feasible(resources, requests) is True

def test_negative_request_amount():
    # Negative Request Amount
    # Constraint: resource requests must be non-negative
    # Reason: invalid input should raise error
    resources = {'cpu': 10}
    requests = [{'cpu': 5}, {'cpu': -2}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)
        
def test_negative_resource_capacity():
    # Negative Resource Capacity
    # Constraint: available resources must be non-negative
    # Reason: invalid system configuration
    resources = {'cpu': -4}
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

def test_empty_requests():
    # Empty Requests
    # Constraint: no demand means always feasible
    # Reason: edge case where nothing is requested
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_unused_resource_in_capacity():
    # Unused Resource in Capacity
    # Constraint: resources can exist without being requested
    # Reason: should still be feasible if unused capacity exists
    resources = {'cpu': 10, 'mem': 20, 'gpu': 2}
    requests = [{'cpu': 3}, {'mem': 5}]
    assert is_allocation_feasible(resources, requests) is True

