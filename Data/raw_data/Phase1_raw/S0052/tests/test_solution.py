## Student Name: Yaseen Ejaz Ahmed
## Student ID: 221608583

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
from EECS4312_Lab5_SpecificationLab_B_221608583.src.solution import is_allocation_feasible
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

def test_exact_capacity_match_multi_resource():
    resources = {'cpu': 6, 'mem': 20}
    requests = [{'cpu': 2, 'mem': 10}, {'cpu': 4, 'mem': 10}]
    assert is_allocation_feasible(resources, requests) is True


def test_empty_requests():
    resources = {'cpu': 5}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_empty_resources_with_requests():
    resources = {}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_negative_request_amount():
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    assert is_allocation_feasible(resources, requests) is False


def test_float_values():
    resources = {'cpu': 5.5}
    requests = [{'cpu': 2.5}, {'cpu': 3.0}]
    assert is_allocation_feasible(resources, requests) is True

