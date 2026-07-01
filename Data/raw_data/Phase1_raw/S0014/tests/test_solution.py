## Student Name: Richard Balroop
## Student ID: 216906349

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

def test_exact_capacity_is_feasible():
    # Sum of requests equals capacity exactly -> feasible
    resources = {"cpu": 10, "mem": 32}
    requests = [{"cpu": 3, "mem": 12}, {"cpu": 7, "mem": 20}]
    assert is_allocation_feasible(resources, requests) is True


def test_empty_requests_is_feasible():
    # No requests -> always feasible if resources are valid
    resources = {"cpu": 5, "mem": 8}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_float_amounts_supported():
    # Floats should work (Number = int | float)
    resources = {"cpu": 5.5}
    requests = [{"cpu": 2.25}, {"cpu": 3.25}]
    assert is_allocation_feasible(resources, requests) is True


def test_non_dict_resources_raises():
    # Structural validation: resources must be a dict
    resources = ["cpu", 5]  # malformed
    requests = [{"cpu": 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_request_amount_raises():
    # Constraint: amounts required must be non-negative
    resources = {"cpu": 5}
    requests = [{"cpu": -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)
        
"""TODO: Add at least 5 additional test cases to test your implementation."""
