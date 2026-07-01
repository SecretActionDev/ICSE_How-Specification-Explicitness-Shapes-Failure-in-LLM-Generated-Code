## Student Name:
## Student ID: 

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
    assert is_allocation_feasible(resources, requests) is False # changed as demand must be less than capacity

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
# AI Recommended test cases:
def test_exact_capacity_should_be_not_be_feasible():
    resources = {'cpu': 12, 'mem': 64}
    requests = [
        {'cpu': 4, 'mem': 16},
        {'cpu': 5, 'mem': 24},
        {'cpu': 3, 'mem': 24},
    ]
    assert is_allocation_feasible(resources, requests) is False # Demand must be less than capacity


def test_empty_requests_list_is_feasible():
    resources = {'cpu': 100, 'gpu': 4}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_empty_resources_with_nonempty_requests_is_infeasible():
    resources = {}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_zero_demand_request_should_be_allowed():
    resources = {'cpu': 8}
    requests = [
        {'cpu': 0},
        {'cpu': 0},
        {'cpu': 7}, #altered as demand must be less than capacity
    ]
    assert is_allocation_feasible(resources, requests) is True


def test_negative_values_are_rejected():
    resources = {'cpu': 10}
    requests = [{'cpu': -3}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

def test_all_requests_have_no_resources_keys():
    resources = {'cpu': 10, 'mem': 32}
    requests = [{}, {}, {}]  # empty dicts
    assert is_allocation_feasible(resources, requests) is True

def test_exact_capacity_should_be_infeasible():
    # New rule: exact consumption of ALL resources → False
    resources = {'cpu': 12, 'mem': 64}
    requests = [
        {'cpu': 4, 'mem': 16},
        {'cpu': 5, 'mem': 24},
        {'cpu': 3, 'mem': 24},
    ]
    assert is_allocation_feasible(resources, requests) is False


def test_empty_requests_list_is_feasible():
    # Still True (resources remain completely unallocated)
    resources = {'cpu': 100, 'gpu': 4}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_empty_resources_with_nonempty_requests_is_infeasible():
    resources = {}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_full_consumption_single_resource_infeasible():
    # New requirement test
    resources = {'cpu': 8}
    requests = [{'cpu': 0}, {'cpu': 0}, {'cpu': 8}]
    assert is_allocation_feasible(resources, requests) is False


def test_one_resource_left_unallocated_is_feasible():
    # New requirement: as long as ≥1 resource has slack, OK
    resources = {'cpu': 10, 'mem': 30}
    requests = [{'cpu': 10, 'mem': 15}]
    assert is_allocation_feasible(resources, requests) is True


def test_all_resources_fully_consumed_infeasible():
    # New requirement: everything used up → False
    resources = {'cpu': 10, 'mem': 30}
    requests = [{'cpu': 10}, {'mem': 30}]
    assert is_allocation_feasible(resources, requests) is False


def test_all_requests_have_no_resources_keys():
    resources = {'cpu': 10, 'mem': 32}
    requests = [{}, {}, {}]
    assert is_allocation_feasible(resources, requests) is True