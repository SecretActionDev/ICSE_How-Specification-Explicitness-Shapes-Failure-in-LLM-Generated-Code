## Student Name:
## Student ID: 

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
# """
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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

def test_allocation_exact_capacity_match():
    resources = {"CPU": 8, "RAM": 16}
    requests = [
        {"CPU": 3, "RAM": 6},
        {"CPU": 5, "RAM": 10}
    ]

    assert is_allocation_feasible(resources, requests) is True
def test_multiple_requests_multiple_resources():
    resources = {"CPU": 10, "RAM": 32, "DISK": 100}
    requests = [
        {"CPU": 2, "RAM": 8},
        {"CPU": 4, "DISK": 40},
        {"RAM": 16, "DISK": 50}
    ]

    assert is_allocation_feasible(resources, requests) is True
def test_request_for_unavailable_resource():
    resources = {"CPU": 4, "RAM": 8}
    requests = [
        {"CPU": 2},
        {"GPU": 1}
    ]

    assert is_allocation_feasible(resources, requests) is False


def test_negative_request_amount():
    resources = {"CPU": 4}
    requests = [
        {"CPU": -1}
    ]

    assert is_allocation_feasible(resources, requests) is False

def test_empty_requests_list():
    resources = {"CPU": 4, "RAM": 8}
    requests = []

    assert is_allocation_feasible(resources, requests) is True


# ==================== EDGE CASES ====================

def test_empty_resources_with_empty_requests():
    # Edge case: both resources and requests are empty
    # Constraint: no resources to allocate, no requests to satisfy
    # Reason: should be trivially feasible
    resources = {}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_empty_request_dict_in_list():
    # Edge case: request list contains an empty dictionary
    # Constraint: empty request requires nothing
    # Reason: should still be feasible
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {}, {'cpu': 2}]
    assert is_allocation_feasible(resources, requests) is True


def test_negative_capacity_in_resources():
    # Edge case: negative capacity value
    # Constraint: capacities must be non-negative
    # Reason: defensive check should return False
    resources = {'cpu': -5}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_zero_capacity_resource_with_zero_request():
    # Boundary: zero capacity with zero demand
    # Constraint: 0 <= 0 should be feasible
    # Reason: boundary condition check
    resources = {'cpu': 0}
    requests = [{'cpu': 0}]
    assert is_allocation_feasible(resources, requests) is True


def test_zero_capacity_resource_with_positive_request():
    # Boundary: zero capacity with positive demand
    # Constraint: any positive demand exceeds zero capacity
    # Reason: should be infeasible
    resources = {'cpu': 0}
    requests = [{'cpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_request_with_zero_amount():
    # Edge case: request asks for zero of a resource
    # Constraint: zero request should not affect feasibility
    # Reason: valid request pattern
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 0, 'mem': 5}, {'cpu': 3, 'mem': 0}]
    assert is_allocation_feasible(resources, requests) is True


def test_float_capacities_and_requests():
    # Edge case: float values for capacities and requests
    # Constraint: function should handle floats correctly
    # Reason: Number type includes float
    resources = {'cpu': 10.5, 'mem': 20.75}
    requests = [{'cpu': 5.25, 'mem': 10.5}, {'cpu': 5.25, 'mem': 10.25}]
    assert is_allocation_feasible(resources, requests) is True


def test_float_exceeds_capacity_slightly():
    # Boundary: float precision edge case
    # Constraint: sum exceeds capacity by small float amount
    # Reason: test float accumulation
    resources = {'cpu': 10.0}
    requests = [{'cpu': 5.1}, {'cpu': 5.0}]
    assert is_allocation_feasible(resources, requests) is False


def test_single_request_exactly_at_capacity():
    # Boundary: single request equals capacity exactly
    # Constraint: demand == capacity should be feasible
    # Reason: boundary condition
    resources = {'cpu': 100}
    requests = [{'cpu': 100}]
    assert is_allocation_feasible(resources, requests) is True


def test_single_request_exceeds_capacity_by_one():
    # Boundary: single request exceeds capacity by minimal amount
    # Constraint: demand > capacity by 1
    # Reason: boundary condition
    resources = {'cpu': 100}
    requests = [{'cpu': 101}]
    assert is_allocation_feasible(resources, requests) is False


def test_cumulative_exceeds_capacity():
    # Edge case: individual requests are fine, but cumulative exceeds
    # Constraint: sum of demands > capacity
    # Reason: test accumulation logic
    resources = {'cpu': 10}
    requests = [{'cpu': 4}, {'cpu': 4}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is False


def test_partial_resource_request():
    # Edge case: requests don't use all available resources
    # Constraint: unused resources should not affect feasibility
    # Reason: partial allocation pattern
    resources = {'cpu': 10, 'mem': 20, 'disk': 100}
    requests = [{'cpu': 5}, {'mem': 10}]
    assert is_allocation_feasible(resources, requests) is True


def test_many_small_requests():
    # Non-functional: performance with many requests
    # Constraint: should handle large number of requests
    # Reason: stress test / code coverage
    resources = {'cpu': 1000}
    requests = [{'cpu': 1} for _ in range(1000)]
    assert is_allocation_feasible(resources, requests) is True


def test_many_small_requests_exceeds():
    # Non-functional: many requests that exceed capacity
    # Constraint: early exit optimization
    # Reason: test early termination
    resources = {'cpu': 500}
    requests = [{'cpu': 1} for _ in range(1000)]
    assert is_allocation_feasible(resources, requests) is False


# ==================== INPUT VALIDATION TESTS ====================

def test_string_as_request_raises():
    # Structural validation: string instead of dict
    # Constraint: request must be a dict
    # Reason: test type validation
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, "invalid"]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_none_as_request_raises():
    # Structural validation: None instead of dict
    # Constraint: request must be a dict
    # Reason: test type validation
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, None]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_tuple_as_request_raises():
    # Structural validation: tuple instead of dict
    # Constraint: request must be a dict
    # Reason: test type validation  
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, ('cpu', 3)]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_integer_as_request_raises():
    # Structural validation: integer instead of dict
    # Constraint: request must be a dict
    # Reason: test type validation
    resources = {'cpu': 10}
    requests = [5]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# ==================== MULTI-RESOURCE EDGE CASES ====================

def test_all_resources_at_exact_capacity():
    # Boundary: all resources exactly meet capacity
    # Constraint: all demands == all capacities
    # Reason: multi-resource boundary test
    resources = {'cpu': 10, 'mem': 20, 'disk': 30}
    requests = [
        {'cpu': 5, 'mem': 10, 'disk': 15},
        {'cpu': 5, 'mem': 10, 'disk': 15}
    ]
    assert is_allocation_feasible(resources, requests) is True


def test_first_resource_fails_immediately():
    # Edge case: first request already exceeds capacity
    # Constraint: early exit on first check
    # Reason: test early termination path
    resources = {'cpu': 5}
    requests = [{'cpu': 10}]
    assert is_allocation_feasible(resources, requests) is False


def test_mixed_int_and_float():
    # Edge case: mix of int and float values
    # Constraint: Number type union handling
    # Reason: type compatibility
    resources = {'cpu': 10, 'mem': 15.5}
    requests = [{'cpu': 5.5, 'mem': 7}, {'cpu': 4, 'mem': 8.5}]
    assert is_allocation_feasible(resources, requests) is True


def test_large_numbers():
    # Non-functional: very large numbers
    # Constraint: should handle large values without overflow
    # Reason: robustness test
    resources = {'cpu': 10**12}
    requests = [{'cpu': 10**11}, {'cpu': 10**11}]
    assert is_allocation_feasible(resources, requests) is True


def test_large_numbers_exceeds():
    # Non-functional: large numbers that exceed
    # Constraint: should correctly detect overflow
    # Reason: robustness test
    resources = {'cpu': 10**12}
    requests = [{'cpu': 6 * 10**11}, {'cpu': 6 * 10**11}]
    assert is_allocation_feasible(resources, requests) is False


def test_only_one_resource_overloaded_of_many():
    # Edge case: multiple resources, only one fails
    # Constraint: any single resource exceeding makes it infeasible
    # Reason: per-resource check
    resources = {'cpu': 10, 'mem': 20, 'disk': 30, 'net': 40}
    requests = [
        {'cpu': 5, 'mem': 10, 'disk': 15, 'net': 20},
        {'cpu': 5, 'mem': 10, 'disk': 16, 'net': 20}  # disk exceeds by 1
    ]
    assert is_allocation_feasible(resources, requests) is False


def test_request_missing_some_resources():
    # Edge case: some requests don't include all resources
    # Constraint: partial requests should be valid
    # Reason: realistic usage pattern
    resources = {'cpu': 10, 'mem': 20}
    requests = [
        {'cpu': 3},           # only cpu
        {'mem': 10},          # only mem
        {'cpu': 2, 'mem': 5}  # both
    ]
    assert is_allocation_feasible(resources, requests) is True
