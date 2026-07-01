## Student Name: Mohsen Maoodhah
## Student ID: 220153425

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
    # This was set to True for the last lab however for this one it should be false as all resources are consumed
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

# My tests
def test1():
    resources = {'cpu': 4, 'gpu': 7}
    requests = [{'cpu': 2}, {'cpu': 2}, {'gpu': 3}]
    assert is_allocation_feasible(resources, requests) is True

def test():
    resources = {'cpu': 6}
    requests = [{'cpu': 5}, {'mem': 4}]
    assert is_allocation_feasible(resources, requests) is False
# ChatGPT's tests

def test_no_requests_is_feasible():
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_request_exceeds_capacity():
    resources = {'cpu': 6}
    requests = [{'cpu': 3}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is False


def test_request_with_non_numeric_amount_raises():
    resources = {'cpu': 10}
    requests = [{'cpu': 5}, {'cpu': 'ten'}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

def test_exact_consumption_single_resource_now_invalid():
    resources = {"cpu": 4}
    requests = [{"cpu": 2}, {"cpu": 2}]
    assert is_allocation_feasible(resources, requests) is False

def test_exact_consumption_multi_resource_now_invalid():
    resources = {"cpu": 4, "gpu": 2}
    requests = [{"cpu": 4}, {"gpu": 2}]
    assert is_allocation_feasible(resources, requests) is False

def test_leaves_leftover_in_unused_resource_valid():
    resources = {"cpu": 4, "gpu": 2}
    requests = [{"cpu": 4}]
    assert is_allocation_feasible(resources, requests) is True

def test_leaves_leftover_by_underusing_capacity_valid():
    resources = {"cpu": 4}
    requests = [{"cpu": 3}]
    assert is_allocation_feasible(resources, requests) is True
