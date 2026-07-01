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
def test_non_str_resource_raises():
    # Non-Dict Resource Raises Error
    # Constraint: structural validation
    # Reason: resource name must be string
    resources = {'cpu': 5}
    requests = [{8 : 2}, {'mem', 1}]  # Malformed Resource
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

def test_non_int_value_raises():
    # Non-Int Resource Value Raises Error
    # Constraint: structural validation
    # Reason: resource value must be int
    resources = {'cpu': 5}
    requests = [{8 : 'cpu'}, {'mem', 1}]  # Malformed Resource Value
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

def test_negative_value_resource():
    # Basic Feasible Single-Resource
    # Constraint: Valid value
    # Reason: Value of resource must be non-negative
    resources = {'cpu': 10}
    requests = [{'cpu': -3}, {'cpu': 4}, {'cpu': 3}]
    assert is_allocation_feasible(resources, requests) is False

def test_non_dict_available_resource_raises():
    # Non-Dict Resource Raises Error
    # Constraint: structural validation
    # Reason: To ensure available resources is well formed.
    resources = ['cpu', 5]
    requests = [{'cpu': 2}, {'mem', 1}]  # Malformed Resource
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

def test_non_str_available_resource_raises():
    # Non-Dict Resource Raises Error
    # Constraint: structural validation
    # Reason: resource name must be string
    resources = {2.2: 5}
    requests = [{'cpu': 2}, {'mem', 1}]  # Malformed Resource
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

# Would've of created a test that would test the invariant of having one resource unallocated.
