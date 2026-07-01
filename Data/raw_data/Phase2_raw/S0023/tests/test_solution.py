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

"""TODO: Add at least 5 additional test cases to test your implementation."""
def test_feasible_allocation_under_capacity():
    """Test 1: Requests are within limits, leaving some resources unallocated."""
    resources = {"CPU": 10, "RAM": 32, "Disk": 100}
    requests = [
        {"CPU": 2, "RAM": 4},
        {"CPU": 4, "RAM": 16, "Disk": 50},
    ]
    # Total needed: CPU=6, RAM=20, Disk=50. 
    # Leftover: CPU=4, RAM=12, Disk=50. (Valid: unallocated resources exist)
    assert is_allocation_feasible(resources, requests) is True

def test_infeasible_allocation_exceeds_capacity():
    """Test 2: Total requests exceed the available capacity."""
    resources = {"CPU": 10, "RAM": 32}
    requests = [
        {"CPU": 6, "RAM": 20},
        {"CPU": 5, "RAM": 10} 
    ]
    assert is_allocation_feasible(resources, requests) is False

def test_infeasible_request_for_missing_resource():
    """Test 3: A request asks for a resource that doesn't exist."""
    resources = {"CPU": 10, "RAM": 32}
    requests = [
        {"CPU": 2, "GPU": 1} 
    ]
    assert is_allocation_feasible(resources, requests) is False

def test_empty_requests_list():
    """Test 4: An empty list of requests leaves all resources unallocated."""
    resources = {"CPU": 10, "RAM": 32}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_raises_value_error_on_invalid_request_type():
    """Test 5: The function raises a ValueError if a request is not a dictionary."""
    resources = {"CPU": 10, "RAM": 32}
    requests = [
        {"CPU": 2},
        "I need 4 CPUs please"
    ]
    with pytest.raises(ValueError, match="Request is not a dictionary."):
        is_allocation_feasible(resources, requests)

def test_infeasible_exact_allocation():
    """Test 6 (NEW): Total requests exactly consume ALL available resources."""
    resources = {"CPU": 10, "RAM": 32}
    requests = [
        {"CPU": 5, "RAM": 16},
        {"CPU": 5, "RAM": 16}
    ]
    # Total needed: CPU=10, RAM=32. 
    # Leftover: CPU=0, RAM=0. (Invalid: no unallocated resources remain)
    assert is_allocation_feasible(resources, requests) is False