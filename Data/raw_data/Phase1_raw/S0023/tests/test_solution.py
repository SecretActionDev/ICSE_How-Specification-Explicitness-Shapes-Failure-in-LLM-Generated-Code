## Student Name: Isaiah Gocool
## Student ID: 218918052

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
def test_feasible_allocation_under_capacity():
    """Test 1: Requests are well within the available resource limits."""
    resources = {"CPU": 10, "RAM": 32, "Disk": 100}
    requests = [
        {"CPU": 2, "RAM": 4},
        {"CPU": 4, "RAM": 16, "Disk": 50},
        {"CPU": 1}
    ]
    # Total needed: CPU=7, RAM=20, Disk=50. All within limits.
    assert is_allocation_feasible(resources, requests) is True

def test_infeasible_allocation_exceeds_capacity():
    """Test 2: Total requests exceed the available capacity of at least one resource."""
    resources = {"CPU": 10, "RAM": 32}
    requests = [
        {"CPU": 6, "RAM": 20},
        {"CPU": 5, "RAM": 10} 
    ]
    # Total needed: CPU=11 (exceeds 10), RAM=30 (within 32).
    assert is_allocation_feasible(resources, requests) is False

def test_infeasible_request_for_missing_resource():
    """Test 3: A request asks for a resource that doesn't exist in the resource pool."""
    resources = {"CPU": 10, "RAM": 32}
    requests = [
        {"CPU": 2, "GPU": 1} # GPU is not in the available resources
    ]
    assert is_allocation_feasible(resources, requests) is False

def test_empty_requests_list():
    """Test 4: An empty list of requests should always be feasible."""
    resources = {"CPU": 10, "RAM": 32}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_raises_value_error_on_invalid_request_type():
    """Test 5: The function should raise a ValueError if a request is not a dictionary."""
    resources = {"CPU": 10, "RAM": 32}
    # The second item in the list is a string, not a dictionary
    requests = [
        {"CPU": 2},
        "I need 4 CPUs please"
    ]
    
    # pytest.raises checks that the specific error is triggered
    with pytest.raises(ValueError, match="Request is not a dictionary."):
        is_allocation_feasible(resources, requests)