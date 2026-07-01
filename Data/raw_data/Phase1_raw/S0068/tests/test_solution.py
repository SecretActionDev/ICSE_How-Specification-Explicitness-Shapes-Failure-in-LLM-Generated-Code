## Student Name: Vikram Singh Chauhan
## Student ID: 220914867
import pytest
from src.solution import is_allocation_feasible

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
    # Reason: allocation must be infeasible (capacity assumed 0)
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_non_dict_request_raises():
    # Non-Dict Request Raises Error
    # Constraint: structural validation
    # Reason: request must be a dict
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]  # Malformed request (list instead of dict)
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)

# Additional Edge Cases

def test_empty_requests_always_feasible():
    """Test that an empty list of requests is always feasible."""
    resources = {'cpu': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_exact_capacity_match():
    """Test boundary condition where demand equals exactly the capacity."""
    resources = {'cpu': 10, 'mem': 16}
    requests = [{'cpu': 5, 'mem': 8}, {'cpu': 5, 'mem': 8}]
    assert is_allocation_feasible(resources, requests) is True

def test_floating_point_resources():
    """Test that the function handles floating point values correctly."""
    resources = {'bandwidth': 10.5}
    requests = [{'bandwidth': 5.2}, {'bandwidth': 5.2}] # Total 10.4
    assert is_allocation_feasible(resources, requests) is True

def test_partial_resource_overlap():
    """Test requests that use different subsets of available resources."""
    resources = {'cpu': 10, 'gpu': 5, 'disk': 100}
    requests = [
        {'cpu': 5},            # Uses only CPU
        {'gpu': 2, 'disk': 50} # Uses GPU and Disk, no CPU
    ]
    assert is_allocation_feasible(resources, requests) is True

def test_zero_capacity_resource():
    """Test that requests for a resource with 0 capacity fail."""
    resources = {'cpu': 0}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_request_exceeds_missing_resource():
    """Test implicit 0 capacity for missing resources."""
    resources = {'cpu': 10}
    # 'ram' is not in resources, so capacity is 0. Requesting 5 should fail.
    requests = [{'cpu': 1, 'ram': 5}] 
    assert is_allocation_feasible(resources, requests) is False
