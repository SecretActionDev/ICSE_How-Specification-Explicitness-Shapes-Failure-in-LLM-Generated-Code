## Student Name: Sanjay Raveendran
## Student ID: 217975467

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
from solution import is_allocation_feasible
import pytest
from solution import is_allocation_feasible

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
def test_empty_requests_are_feasible():
    """
    No requests should always be feasible as no resources are consumed.
    """
    resources = {"cpu": 4, "mem": 16}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_exact_capacity_match():
    """
    Allocation is feasible when total demand exactly equals capacity.
    """
    resources = {"cpu": 6}
    requests = [{"cpu": 2}, {"cpu": 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_request_with_multiple_resources_feasible():
    """
    Single request requiring multiple resources within capacity.
    """
    resources = {"cpu": 8, "mem": 32}
    requests = [{"cpu": 4, "mem": 16}]
    assert is_allocation_feasible(resources, requests) is True


def test_multiple_resources_one_exact_one_under():
    """
    One resource exactly meets capacity while another stays under.
    """
    resources = {"cpu": 5, "mem": 10}
    requests = [{"cpu": 3, "mem": 4}, {"cpu": 2, "mem": 5}]
    assert is_allocation_feasible(resources, requests) is True


def test_zero_capacity_resource_requested():
    """
    Requesting a resource with zero capacity should be infeasible.
    """
    resources = {"cpu": 0}
    requests = [{"cpu": 1}]
    assert is_allocation_feasible(resources, requests) is False
def test_single_resource_feasible():
    resources = {"cpu": 10}
    requests = [{"cpu": 3}, {"cpu": 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_single_resource_infeasible():
    resources = {"cpu": 5}
    requests = [{"cpu": 3}, {"cpu": 4}]
    assert is_allocation_feasible(resources, requests) is False


# ---------- MULTI-RESOURCE CASES ----------

def test_multi_resource_all_feasible():
    resources = {"cpu": 8, "mem": 32}
    requests = [{"cpu": 2, "mem": 8}, {"cpu": 4, "mem": 16}]
    assert is_allocation_feasible(resources, requests) is True


def test_multi_resource_one_exceeds_capacity():
    resources = {"cpu": 8, "mem": 30}
    requests = [{"cpu": 2, "mem": 10}, {"cpu": 6, "mem": 25}]
    assert is_allocation_feasible(resources, requests) is False


# ---------- RESOURCE EXISTENCE ----------

def test_request_for_missing_resource():
    resources = {"cpu": 10}
    requests = [{"cpu": 2}, {"gpu": 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_request_subset_of_resources():
    resources = {"cpu": 10, "mem": 32}
    requests = [{"cpu": 5}]
    assert is_allocation_feasible(resources, requests) is True


# ---------- STRUCTURAL VALIDATION ----------

def test_non_dict_request_raises_value_error():
    resources = {"cpu": 5}
    requests = [{"cpu": 2}, ["mem", 1]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_all_requests_must_be_dicts_even_if_one_is_invalid():
    resources = {"cpu": 5}
    requests = [["cpu", 2]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# ---------- EDGE CASES ----------

def test_empty_requests_list():
    resources = {"cpu": 4, "mem": 16}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_exact_capacity_match():
    resources = {"cpu": 6}
    requests = [{"cpu": 2}, {"cpu": 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_zero_capacity_resource_requested():
    resources = {"cpu": 0}
    requests = [{"cpu": 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_zero_capacity_resource_not_requested():
    resources = {"cpu": 0}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


# ---------- CONSISTENCY / INVARIANTS ----------

def test_usage_accumulates_across_requests():
    resources = {"cpu": 10}
    requests = [{"cpu": 3}, {"cpu": 3}, {"cpu": 3}]
    assert is_allocation_feasible(resources, requests) is True


def test_order_of_requests_does_not_matter():
    resources = {"cpu": 6}
    requests1 = [{"cpu": 2}, {"cpu": 4}]
    requests2 = [{"cpu": 4}, {"cpu": 2}]
    assert is_allocation_feasible(resources, requests1) == is_allocation_feasible(resources, requests2)
