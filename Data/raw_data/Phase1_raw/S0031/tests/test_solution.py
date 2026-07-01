## Student Name: George Yousif
## Student ID: 215554413

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

def test_empty_requests_is_feasible():
    # No requests means nothing to allocate => always feasible (assuming resources are valid)
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_request_can_omit_some_resources():
    # Requests don't have to mention every resource; omitted resources mean 0 usage
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 2}, {'mem': 3}]
    assert is_allocation_feasible(resources, requests) is True


def test_float_amounts_boundary_feasible():
    # Floats are allowed; total exactly equal to capacity should still be feasible
    resources = {'cpu': 1.5}
    requests = [{'cpu': 0.5}, {'cpu': 1.0}]
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    # Negative resource amounts are invalid input => should raise ValueError
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_non_numeric_request_amount_raises():
    # Non-numeric resource amounts are invalid => should raise ValueError
    resources = {'cpu': 5}
    requests = [{'cpu': "two"}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)