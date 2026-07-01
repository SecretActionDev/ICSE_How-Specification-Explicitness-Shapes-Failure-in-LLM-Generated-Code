## Student Name: Elim Lemango
## Student ID: 216689424

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
    # Constraint: at least one resource must remain unallocated
    # Reason: fully allocating cpu is now infeasible
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
    requests = [{'cpu': 2}, ['mem', 1]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_exact_capacity_boundary():
    # Exact Capacity Boundary
    # Constraint: at least one resource must remain unallocated
    # Reason: total demand equals capacity → now infeasible
    resources = {'cpu': 6}
    requests = [{'cpu': 2}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is False


def test_empty_requests_list():
    # Empty Requests
    # Constraint: at least one resource must remain unallocated
    # Reason: nothing allocated → all resources remain available
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    # Negative Request Amount
    # Constraint: requests must be non-negative
    # Reason: negative allocation is invalid input
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_resource_capacity_raises():
    # Negative Resource Capacity
    # Constraint: resource capacities must be non-negative
    # Reason: invalid availability definition
    resources = {'cpu': -5}
    requests = [{'cpu': 2}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_zero_capacity_resource():
    # Zero Capacity Resource
    # Constraint: zero-capacity resources cannot be allocated
    # Reason: any positive demand should make allocation infeasible
    resources = {'cpu': 0}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False