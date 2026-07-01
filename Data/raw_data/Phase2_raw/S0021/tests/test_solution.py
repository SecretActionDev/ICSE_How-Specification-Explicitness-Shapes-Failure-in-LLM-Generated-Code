# Student Name:
# Student ID:

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
    # Constraint: demand < capacity so some resource remains
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_single_resource_exact_capacity_invalid():
    # Exact Capacity Usage (Single Resource)
    # Constraint: cannot consume all resources
    resources = {'cpu': 6}
    requests = [{'cpu': 2}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is False


def test_multi_resource_infeasible_one_overloaded():
    # Multi-Resource Infeasible (one overload)
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {
        'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False


def test_all_resources_fully_consumed_invalid():
    # All resources exactly consumed
    # New requirement: at least one must remain unused
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 3, 'mem': 10}, {'cpu': 5, 'mem': 20}]
    assert is_allocation_feasible(resources, requests) is False


def test_one_resource_remaining_valid():
    # One resource fully used but another still available
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 8, 'mem': 20}]
    assert is_allocation_feasible(resources, requests) is True


def test_missing_resource_in_availability():
    # Request references unavailable resource
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_empty_requests_feasible():
    # No requests means all resources remain unused
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_non_dict_request_raises():
    # Structural validation
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_request_amount_raises():
    # Invalid negative demand
    resources = {'cpu': 10}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_resource_capacity_raises():
    # Invalid negative capacity
    resources = {'cpu': -5}
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_single_resource_exact_capacity_invalid():
    # Single resource fully consumed -> invalid
    resources = {'cpu': 5}
    requests = [{'cpu': 5}]
    assert is_allocation_feasible(resources, requests) is False


def test_single_resource_less_than_capacity_valid():
    # Single resource not fully consumed -> valid
    resources = {'cpu': 5}
    requests = [{'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_multiple_resources_all_fully_consumed_invalid():
    # Every resource fully consumed -> invalid
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 5, 'mem': 10}]
    assert is_allocation_feasible(resources, requests) is False


def test_multiple_resources_one_remaining_valid():
    # One resource fully consumed but another remains -> valid
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 5, 'mem': 8}]
    assert is_allocation_feasible(resources, requests) is True


def test_multiple_resources_none_fully_consumed_valid():
    # All resources still have remaining capacity -> valid
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 3, 'mem': 6}]
    assert is_allocation_feasible(resources, requests) is True


def test_zero_requests_all_resources_remaining_valid():
    # No allocation means all resources remain -> valid
    resources = {'cpu': 4, 'mem': 8}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_three_resources_two_full_one_remaining_valid():
    # Two resources fully used but one still remaining -> valid
    resources = {'cpu': 5, 'mem': 10, 'gpu': 4}
    requests = [{'cpu': 5, 'mem': 10, 'gpu': 2}]
    assert is_allocation_feasible(resources, requests) is True


def test_three_resources_all_exact_invalid():
    # All resources exactly consumed -> invalid
    resources = {'cpu': 5, 'mem': 10, 'gpu': 4}
    requests = [{'cpu': 5, 'mem': 10, 'gpu': 4}]
    assert is_allocation_feasible(resources, requests) is False
