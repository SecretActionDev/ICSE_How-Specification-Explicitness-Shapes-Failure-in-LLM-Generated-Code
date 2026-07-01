## Student Name:
## Student ID: 

"""
Student test suite for the is_allocation_feasible exercise.

Contains at least 5 additional test cases to verify the implementation.
"""
from solution import is_allocation_feasible
import pytest


def test_empty_requests_feasible():
    # Empty Requests Feasible
    # Constraint: no requests means no demand
    # Reason: edge case - empty request list should be feasible
    resources = {'cpu': 10, 'mem': 20}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_exact_capacity_match():
    # Exact Capacity Match
    # Constraint: total demand exactly equals capacity
    # Reason: boundary case - should be feasible when demand equals capacity
    resources = {'cpu': 10, 'mem': 15}
    requests = [{'cpu': 5, 'mem': 8}, {'cpu': 5, 'mem': 7}]
    assert is_allocation_feasible(resources, requests) is True


def test_single_request_exceeds_capacity():
    # Single Request Exceeds Capacity
    # Constraint: one request exceeds available capacity
    # Reason: check detection when a single request is too large
    resources = {'cpu': 5, 'mem': 10}
    requests = [{'cpu': 6, 'mem': 5}]
    assert is_allocation_feasible(resources, requests) is False


def test_float_values():
    # Float Values
    # Constraint: function should handle float values correctly
    # Reason: verify support for non-integer resource amounts
    resources = {'cpu': 10.5, 'mem': 20.0}
    requests = [{'cpu': 3.2, 'mem': 5.5}, {'cpu': 4.3, 'mem': 6.5}]
    assert is_allocation_feasible(resources, requests) is True


def test_float_values_infeasible():
    # Float Values Infeasible
    # Constraint: float values that exceed capacity
    # Reason: verify float comparison works correctly for infeasible cases
    resources = {'cpu': 10.0, 'mem': 20.0}
    requests = [{'cpu': 5.5, 'mem': 10.0}, {'cpu': 5.0, 'mem': 11.0}]
    assert is_allocation_feasible(resources, requests) is False

