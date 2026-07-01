## Student Name: Matthew Magagna
## Student ID: 219804921

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
    # Constraint: total demand <= capacity AND at least one unit remains unallocated
    # Reason: check basic functional requirement with new slack rule
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 2}]  # total 9, leaves 1
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


def test_exact_capacity_boundary_now_infeasible():
    # Exact Capacity Boundary (NEW RULE)
    # Constraint: consuming all available resources is not allowed
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, {'cpu': 3}]  # total 5, leaves 0
    assert is_allocation_feasible(resources, requests) is False


def test_empty_requests_feasible_if_any_capacity_positive():
    # Empty Requests
    # Constraint: if any capacity > 0, then resources remain unallocated
    resources = {'cpu': 0, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_empty_requests_infeasible_if_all_zero_capacity():
    # Empty Requests with all-zero capacities (NEW RULE)
    # Constraint: must leave at least one unit unallocated, impossible if all caps are 0
    resources = {'cpu': 0, 'mem': 0}
    requests = []
    assert is_allocation_feasible(resources, requests) is False


def test_request_missing_some_resources_ok_and_slack_exists():
    # Request Missing Some Resources
    # Constraint: missing keys imply 0 usage; slack must still exist somewhere
    resources = {'cpu': 4, 'mem': 10}
    requests = [{'cpu': 2}, {'mem': 5}]
    assert is_allocation_feasible(resources, requests) is True


def test_slack_in_one_resource_is_enough():
    # Slack in only one resource is sufficient (NEW RULE)
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 5, 'mem': 7}]  # cpu fully used, mem has slack
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_infeasible():
    # Negative Request
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    assert is_allocation_feasible(resources, requests) is False


def test_negative_capacity_infeasible():
    # Negative Capacity
    resources = {'cpu': -5}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_float_amounts_supported_and_slack_exists():
    # Float Amounts Supported
    resources = {'cpu': 1.0}
    requests = [{'cpu': 0.4}, {'cpu': 0.5}]  # total 0.9, leaves 0.1
    assert is_allocation_feasible(resources, requests) is True


def test_float_exact_fill_now_infeasible():
    # Float exact fill (NEW RULE)
    resources = {'cpu': 1.0}
    requests = [{'cpu': 0.4}, {'cpu': 0.6}]  # total 1.0, leaves 0.0
    assert is_allocation_feasible(resources, requests) is False


def test_amount_non_numeric_infeasible():
    # Non-Numeric Amount
    resources = {'cpu': 5}
    requests = [{'cpu': "2"}]
    assert is_allocation_feasible(resources, requests) is False
