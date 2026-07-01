## Student Name: Dexter Sargent
## Student ID: 217931460

"""
Public test suite for the allocation feasibility exercise.

Students can run these tests locally to check correctness of their implementation.
The hidden test suite used for grading contains additional edge cases.

Updated Requirement:
- At least one resource must remain partially unallocated after assignment.
  If all resources are exactly consumed, the allocation is infeasible.
"""

from src.solution import is_allocation_feasible
import pytest


# ---------------------------
# Original Functional Tests
# ---------------------------

def test_basic_feasible_single_resource():
    # total demand < capacity (leftover exists)
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_multi_resource_infeasible_one_overloaded():
    # one resource exceeds capacity
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8},
                {'cpu': 3, 'mem': 10},
                {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False


def test_missing_resource_in_availability():
    # request references unavailable resource
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_non_dict_request_raises():
    # malformed request structure
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# ---------------------------
# Validation & Edge Cases
# ---------------------------

def test_empty_requests():
    # no demand → leftover exists → valid
    resources = {'cpu': 10, 'mem': 20}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_non_numeric_request_value_raises():
    resources = {'cpu': 5}
    requests = [{'cpu': 'two'}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# ---------------------------
# Updated Exact-Consumption Behavior
# ---------------------------

def test_exact_consumption_single_resource_not_allowed():
    resources = {'cpu': 10}
    requests = [{'cpu': 4}, {'cpu': 6}]
    assert is_allocation_feasible(resources, requests) is False


def test_all_resources_fully_consumed_not_allowed():
    resources = {'cpu': 10, 'mem': 20}
    requests = [{'cpu': 10, 'mem': 20}]
    assert is_allocation_feasible(resources, requests) is False


def test_floating_point_resources_exact_consumption_not_allowed():
    resources = {'cpu': 5.5, 'mem': 10.0}
    requests = [{'cpu': 2.5, 'mem': 4.0},
                {'cpu': 3.0, 'mem': 6.0}]
    assert is_allocation_feasible(resources, requests) is False


def test_large_numbers_exact_consumption_not_allowed():
    resources = {'cpu': 1e12}
    requests = [{'cpu': 4e11}, {'cpu': 6e11}]
    assert is_allocation_feasible(resources, requests) is False


# ---------------------------
# Leftover Rule Verification
# ---------------------------

def test_one_resource_leftover_allowed():
    resources = {'cpu': 10, 'mem': 20}
    requests = [{'cpu': 10, 'mem': 15}]
    assert is_allocation_feasible(resources, requests) is True


def test_partial_usage_all_resources_allowed():
    resources = {'cpu': 10, 'mem': 20}
    requests = [{'cpu': 5, 'mem': 10}]
    assert is_allocation_feasible(resources, requests) is True