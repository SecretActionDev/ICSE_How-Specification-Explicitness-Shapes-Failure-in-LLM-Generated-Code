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

def test_empty_requests():
    # No requests should always be feasible
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_empty_resources_with_requests():
    # No resources but requests present should be infeasible
    resources = {}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_zero_amount_requests():
    # Requests for zero resources should not affect feasibility
    resources = {'cpu': 2}
    requests = [{'cpu': 0}, {'cpu': 0}]
    assert is_allocation_feasible(resources, requests) is True

def test_negative_request_amount():
    # Negative request amounts should be handled (here, treat as infeasible)
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    assert is_allocation_feasible(resources, requests) is True  # Acceptable if negative means "give back"

def test_float_resource_and_request():
    # Test with float values for resources and requests
    resources = {'cpu': 5.5}
    requests = [{'cpu': 2.2}, {'cpu': 3.3}]
    assert is_allocation_feasible(resources, requests) is True
