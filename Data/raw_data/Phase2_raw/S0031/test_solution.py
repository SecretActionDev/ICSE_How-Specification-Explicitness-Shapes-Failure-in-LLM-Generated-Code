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
    # Constraint: total demand < capacity (must leave at least one unit unused)
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 2}]
    assert is_allocation_feasible(resources, requests) is True


def test_multi_resource_infeasible_one_overloaded():
    # Multi-Resource Infeasible (one overload)
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False


def test_missing_resource_in_availability():
    # Request references unavailable resource
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_non_dict_request_raises():
    # Structural validation: request must be a dict
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_empty_requests_is_feasible():
    # No allocation still leaves all resources unallocated
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_request_can_omit_some_resources():
    # Omitted resources imply zero usage
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 2}, {'mem': 3}]
    assert is_allocation_feasible(resources, requests) is True


def test_exact_capacity_single_resource_is_infeasible():
    # New requirement: must leave at least one resource partially unallocated
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, {'cpu': 3}]
    assert is_allocation_feasible(resources, requests) is False


def test_all_resources_exactly_consumed_is_infeasible():
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 5}, {'mem': 10}]
    assert is_allocation_feasible(resources, requests) is False


def test_at_least_one_resource_left_unallocated():
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 5}]
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_non_numeric_request_amount_raises():
    resources = {'cpu': 5}
    requests = [{'cpu': "two"}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)