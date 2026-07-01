## Student Name: Shrey Grover
## Student ID: 219579143

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
from solution import is_allocation_feasible
import pytest


def test_basic_feasible_single_resource():
   
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 2}]  # total = 9, leaves 1
    assert is_allocation_feasible(resources, requests) is True


def test_multi_resource_infeasible_one_overloaded():

    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False


def test_missing_resource_in_availability():
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_non_dict_request_raises():
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]  # malformed request
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# --- Additional tests ---

def test_infeasible_exact_capacity_boundary_single_resource():
    resources = {'cpu': 10}
    requests = [{'cpu': 6}, {'cpu': 4}]  # total = 10, leaves 0
    assert is_allocation_feasible(resources, requests) is False


def test_feasible_empty_requests():
    resources = {'cpu': 10, 'mem': 20}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_infeasible_single_resource_over_capacity():
    resources = {'cpu': 10}
    requests = [{'cpu': 8}, {'cpu': 3}]  # total = 11 > 10
    assert is_allocation_feasible(resources, requests) is False


def test_negative_request_amount_raises():
    resources = {'cpu': 10}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_resources_not_a_dict_raises():
    resources = [('cpu', 10)]
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_feasible_multi_resource_one_leftover():
    resources = {'cpu': 10, 'mem': 10}
    requests = [{'cpu': 10, 'mem': 7}]  # cpu leftover 0, mem leftover 3
    assert is_allocation_feasible(resources, requests) is True


def test_infeasible_multi_resource_all_consumed():
    resources = {'cpu': 10, 'mem': 10}
    requests = [{'cpu': 4, 'mem': 6}, {'cpu': 6, 'mem': 4}]  # cpu=10, mem=10
    assert is_allocation_feasible(resources, requests) is False
