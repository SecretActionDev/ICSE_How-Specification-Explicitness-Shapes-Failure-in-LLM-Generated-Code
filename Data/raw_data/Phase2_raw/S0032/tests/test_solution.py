## Student Name: Triya Augustine
## Student ID: 218859157

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
    # Constraint: total demand < capacity
    # Reason: check basic functional requirement
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 3}]
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

def test_empty_requests_still_feasible_with_new_rule():
    # Empty Requests
    # Constraint: no resources consumed
    # Reason: all resources remain unallocated
    resources = {'cpu': 10, 'mem': 20}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_zero_amount_request():
    # Zero Amount Request
    # Constraint: zero demand should not affect feasibility
    # Reason: ensure zero values are handled correctly
    resources = {'cpu': 5}
    requests = [{'cpu': 0}, {'cpu': 5}]
    assert is_allocation_feasible(resources, requests) is False


def test_negative_request_amount():
    # Negative Request Amount
    # Constraint: requests must be non-negative
    # Reason: invalid input should be rejected
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    assert is_allocation_feasible(resources, requests) is False


def test_float_resource_values():
    # Floating-Point Resource Values
    # Constraint: support int and float capacities and requests
    # Reason: numeric generality
    resources = {'bandwidth': 10.5}
    requests = [{'bandwidth': 3.5}, {'bandwidth': 7.0}]
    assert is_allocation_feasible(resources, requests) is False


def test_empty_resources_with_requests():
    # Empty Resources with Non-Empty Requests
    # Constraint: cannot satisfy any request without resources
    # Reason: edge case for missing availability
    resources = {}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_all_resources_fully_consumed_single_resource():
    # All Resources Fully Consumed (Single Resource)
    # Constraint: at least one resource must remain unallocated
    # Reason: new requirement
    resources = {'cpu': 10}
    requests = [{'cpu': 5}, {'cpu': 5}]
    assert is_allocation_feasible(resources, requests) is False

def test_all_resources_fully_consumed_multiple_resources():
    # All Resources Fully Consumed (Multiple Resources)
    # Constraint: at least one resource must remain unallocated
    # Reason: new requirement across all resources
    resources = {'cpu': 8, 'mem': 16}
    requests = [{'cpu': 8}, {'mem': 16}]
    assert is_allocation_feasible(resources, requests) is False

def test_one_resource_remains_unallocated():
    # One Resource Remains Unallocated
    # Constraint: at least one resource must remain partially unused
    # Reason: valid allocation under new rule
    resources = {'cpu': 8, 'mem': 16}
    requests = [{'cpu': 8}]
    assert is_allocation_feasible(resources, requests) is True

def test_partial_consumption_single_resource():
    # Partial Consumption
    # Constraint: resource usage must be strictly less than capacity
    # Reason: satisfies leftover requirement
    resources = {'cpu': 10}
    requests = [{'cpu': 6}]
    assert is_allocation_feasible(resources, requests) is True
