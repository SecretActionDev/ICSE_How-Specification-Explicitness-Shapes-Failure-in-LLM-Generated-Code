## Student Name:
## Student ID: 

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
    # Constraint: no demand
    # Reason: zero requests should always be feasible
    resources = {'cpu': 10, 'mem': 20}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    # Negative Request Amount
    # Constraint: negative requests are not allowed
    # Reason: invalid input must raise an error
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_non_numeric_request_value_raises():
    # Non-Numeric Request Value
    # Constraint: request values must be numeric
    # Reason: type safety
    resources = {'cpu': 5}
    requests = [{'cpu': 'two'}]
    with pytest.raises((TypeError, ValueError)):
        is_allocation_feasible(resources, requests)


def test_floating_point_resources_and_requests():
    # Floating-Point Resources and Requests
    # Constraint: floats are allowed
    # Reason: numeric generality
    resources = {'cpu': 5.5, 'mem': 10.0}
    requests = [{'cpu': 2.5, 'mem': 4.0}, {'cpu': 3.0, 'mem': 6.0}]
    assert is_allocation_feasible(resources, requests) is True


def test_large_numbers():
    # Large Numbers
    # Constraint: handle large capacities and demands
    # Reason: stress test arithmetic correctness
    resources = {'cpu': 1e12}
    requests = [{'cpu': 4e11}, {'cpu': 6e11}]
    assert is_allocation_feasible(resources, requests) is True
