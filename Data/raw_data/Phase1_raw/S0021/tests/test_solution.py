# Student Name:
# Student ID:

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
    requests = [{'cpu': 2, 'mem': 8}, {
        'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
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


def test_empty_requests_feasible():
    # Empty Requests
    # Constraint: no demand should always be feasible (given valid resources)
    # Reason: baseline/edge case
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_zero_amounts_feasible():
    # Zero Amount Requests
    # Constraint: zero demand should not consume capacity
    # Reason: ensure zero values are handled correctly
    resources = {'cpu': 2}
    requests = [{'cpu': 0}, {'cpu': 0}]
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    # Negative Amount Raises Error
    # Constraint: request amounts must be non-negative
    # Reason: structural/semantic validation
    resources = {'cpu': 10}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_resource_capacity_raises():
    # Negative Capacity Raises Error
    # Constraint: capacities must be non-negative
    # Reason: structural validation
    resources = {'cpu': -5}
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_non_numeric_capacity_raises():
    # Non-numeric Capacity Raises Error
    # Constraint: capacities must be int/float
    # Reason: type validation for resources
    resources = {'cpu': "10"}  # invalid type
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_non_numeric_request_amount_raises():
    # Non-numeric Request Amount Raises Error
    # Constraint: request amounts must be int/float
    # Reason: type validation for requests
    resources = {'cpu': 10}
    requests = [{'cpu': "2"}]  # invalid type
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_request_equals_capacity_feasible():
    # Exact Capacity Boundary
    # Constraint: total demand == capacity should be feasible
    # Reason: off-by-one / boundary check
    resources = {'cpu': 6}
    requests = [{'cpu': 2}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is True
