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
    # Constraint: at least one resource must remain unallocated
    # Reason: exact-fit allocations are now invalid
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


def test_exact_fit_allocation():
    # Exact-Fit Allocation
    # Constraint: at least one resource must remain unallocated
    # Reason: all resources are fully consumed
    resources = {'cpu': 10, 'mem': 32}
    requests = [
        {'cpu': 4, 'mem': 10},
        {'cpu': 6, 'mem': 22}
    ]
    assert is_allocation_feasible(resources, requests) is False

def test_over_allocation_returns_false():
    resources = {'cpu': 8}
    requests = [
        {'cpu': 3},
        {'cpu': 6}
    ]
    assert is_allocation_feasible(resources, requests) is False
def test_unknown_resource_returns_false():
    resources = {'cpu': 4}
    requests = [{'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False
def test_empty_requests_is_feasible():
    resources = {'cpu': 10, 'mem': 16}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_non_dict_resources_raises():
    resources = ['cpu', 5]  # malformed resources
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# new test cases for the new lab 6 

def test_all_resources_exactly_consumed_is_infeasible():
    # All Resources Fully Consumed
    # Constraint: at least one resource must remain unallocated
    # Reason: consuming all available resources is now invalid
    resources = {'cpu': 4, 'mem': 8}
    requests = [{'cpu': 4, 'mem': 8}]
    assert is_allocation_feasible(resources, requests) is False


def test_one_resource_remaining_is_feasible():
    # One Resource Has Remaining Capacity
    # Constraint: at least one resource must remain unallocated
    # Reason: allocation leaves unused cpu
    resources = {'cpu': 4, 'mem': 8}
    requests = [{'cpu': 3, 'mem': 8}]
    assert is_allocation_feasible(resources, requests) is True


def test_single_resource_exact_fit_is_infeasible():
    # Single Resource Exact Fit
    # Constraint: at least one resource must remain unallocated
    # Reason: single resource is fully consumed
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, {'cpu': 3}]
    assert is_allocation_feasible(resources, requests) is False