## Student Name: Mahnsi Ruparelia
## Student ID: 219107457

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
from src.solution import is_allocation_feasible
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
    # Empty Requests
    resources = {'cpu': 10, 'mem': 20}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_request_with_unmentioned_resource_defaults_to_zero():
    # Partial Resource Usage
    # Constraint: resources not mentioned in a request are treated as 0
    # Reason: ensure function does not incorrectly require all resources per request
    resources = {'cpu': 5, 'mem': 10}
    requests = [
        {'cpu': 3},
        {'mem': 8}
    ]
    assert is_allocation_feasible(resources, requests) is True

def test_negative_request_amount():
    # Negative Request Amount
    # Constraint: resource demands must be non-negative
    # Reason: prevent logically invalid allocations
    resources = {'cpu': 10}
    requests = [{'cpu': -3}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

def test_float_amounts_feasible():
    # Float Resource Amounts
    # Constraint: Number type includes floats, not just ints
    # Reason: ensure float demands are handled correctly and don't cause type errors
    resources = {'cpu': 7.0, 'mem': 10.5}
    requests = [{'cpu': 3.5, 'mem': 4.0}, {'cpu': 3.5, 'mem': 6.5}]
    assert is_allocation_feasible(resources, requests) is True

def test_exact_capacity_boundary():
    # Exact Capacity Match (Boundary)
    # Constraint: total demand == total capacity should be feasible
    # Reason: ensure boundary condition is treated as valid, not incorrectly rejected
    resources = {'cpu': 9, 'mem': 15}
    requests = [{'cpu': 4, 'mem': 7}, {'cpu': 5, 'mem': 8}]
    assert is_allocation_feasible(resources, requests) is True