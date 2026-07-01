## Student Name: Avery Backus
## Student ID: 219767888

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
    resources = {"cpu": 4, "mem": 8}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_exact_capacity_boundary_is_feasible():
    resources = {"cpu": 10}
    requests = [{"cpu": 4}, {"cpu": 6}]
    assert is_allocation_feasible(resources, requests) is True


def test_empty_resources_with_no_requests_is_feasible():
    resources = {}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    resources = {"cpu": 10}
    requests = [{"cpu": -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_resource_capacity_raises():
    resources = {"cpu": -5}
    requests = [{"cpu": 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_float_amounts_feasible():
    resources = {"cpu": 5.0, "mem": 3.5}
    requests = [{"cpu": 1.2, "mem": 1.0}, {"cpu": 3.8, "mem": 2.5}]
    assert is_allocation_feasible(resources, requests) is True

