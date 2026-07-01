
## Student Name: Negar Khalilazar
## Student ID: 221037437
"""TODO: Add at least 5 additional test cases to test your implementation."""

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
from solution import is_allocation_feasible
import pytest


# def test_basic_feasible_single_resource():
#     # Basic Feasible Single-Resource
#     # Constraint: total demand <= capacity
#     # Reason: check basic functional requirement
#     resources = {'cpu': 10}
#     requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 3}]
#     assert is_allocation_feasible(resources, requests) is True

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


def test_infeasible_exceeds_capacity():
    resources = {"cpu": 5}
    requests = [{"cpu": 3}, {"cpu": 3}]
    assert is_allocation_feasible(resources, requests) is False

def test_unknown_resource_fails():
    resources = {"cpu": 5}
    requests = [{"gpu": 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_negative_request_fails():
    resources = {"cpu": 5}
    requests = [{"cpu": -1}]
    assert is_allocation_feasible(resources, requests) is False

def test_invalid_resources_negative_capacity_raises():
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": -1}, [{"cpu": 0}])

def test_invalid_requests_not_a_list_raises():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 5}, {"cpu": 1})

def test_invalid_request_entry_not_a_dict_raises():
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 5}, [("cpu", 1)])

def test_single_resource_with_slack_is_feasible():
    resources = {"cpu": 10}
    requests = [{"cpu": 4}, {"cpu": 5}]
    assert is_allocation_feasible(resources, requests) is True

def test_single_resource_exactly_full_is_infeasible():
    resources = {"cpu": 10}
    requests = [{"cpu": 6}, {"cpu": 4}]
    assert is_allocation_feasible(resources, requests) is False

def test_multi_resource_one_has_slack_is_feasible():
    resources = {"cpu": 8, "mem": 30}
    requests = [{"cpu": 8, "mem": 29}]
    assert is_allocation_feasible(resources, requests) is True

def test_multi_resource_all_exactly_full_is_infeasible():
    resources = {"cpu": 8, "mem": 30}
    requests = [{"cpu": 5, "mem": 10}, {"cpu": 3, "mem": 20}]
    assert is_allocation_feasible(resources, requests) is False

def test_empty_requests_is_feasible_if_resources_positive():
    resources = {"cpu": 5, "mem": 16}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_only_zero_capacity_resource_is_infeasible():
    resources = {"cpu": 0}
    requests = [{"cpu": 0}]
    assert is_allocation_feasible(resources, requests) is False
