## Student Name: Beckham Gahirwa
## Student ID: 220043782

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
def test_empty_requests_is_feasible():
    # No requests should always be feasible
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_exact_capacity_is_feasible():
    # Boundary: exactly equals capacity should be feasible
    resources = {'cpu': 10}
    requests = [{'cpu': 6}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_zero_capacity_with_zero_demand_is_feasible():
    # Zero capacity is fine if demand is zero
    resources = {'cpu': 0}
    requests = [{'cpu': 0}, {'cpu': 0}]
    assert is_allocation_feasible(resources, requests) is True


def test_float_amounts_supported():
    # Your stub allows float; feasibility must work with floats
    resources = {'cpu': 5.5, 'mem': 10.0}
    requests = [{'cpu': 2.25, 'mem': 3.5}, {'cpu': 3.25, 'mem': 6.5}]
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    # Negative demand is nonsensical: should raise
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_capacity_raises():
    # Negative capacity is invalid: should raise
    resources = {'cpu': -5}
    requests = [{'cpu': 0}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)
