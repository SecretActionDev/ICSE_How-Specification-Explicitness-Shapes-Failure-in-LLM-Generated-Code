## Student Name: Beckham Gahirwa
## Student ID: 220043782

"""
Public test suite for the resource allocation feasibility exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
from solution import is_allocation_feasible
import pytest


def test_feasible_single_resource_leaves_leftover():
    # Feasible only if some capacity remains unused
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}]  # total 7, leaves 3
    assert is_allocation_feasible(resources, requests) is True


def test_infeasible_single_resource_exactly_consumes_all():
    # New requirement: consuming all capacity is invalid
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 3}]  # total 10, leaves 0
    assert is_allocation_feasible(resources, requests) is False


def test_multi_resource_infeasible_one_overloaded():
    # Still infeasible if any resource exceeds capacity
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False


def test_multi_resource_feasible_if_at_least_one_resource_leftover():
    # CPU fully used, but mem has leftover => valid
    resources = {'cpu': 10, 'mem': 20}
    requests = [{'cpu': 10, 'mem': 5}]
    assert is_allocation_feasible(resources, requests) is True


def test_multi_resource_infeasible_if_all_resources_exactly_consumed():
    # Even if within capacity, if every resource hits exactly 0 leftover => invalid
    resources = {'cpu': 10, 'mem': 20}
    requests = [{'cpu': 10, 'mem': 20}]
    assert is_allocation_feasible(resources, requests) is False


def test_missing_resource_in_availability():
    # Unknown resource => infeasible
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_non_dict_request_raises():
    # Request must be dict
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_empty_requests_is_feasible_if_resources_exist():
    # With no requests, everything remains unused => satisfies leftover rule
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_zero_capacity_with_zero_demand_is_infeasible_now():
    # New requirement: must leave leftover, but 0 capacity can't leave leftover
    resources = {'cpu': 0}
    requests = [{'cpu': 0}]
    assert is_allocation_feasible(resources, requests) is False


def test_float_amounts_supported_and_leftover_required():
    # Floats supported; must still leave leftover in at least one resource
    resources = {'cpu': 5.5, 'mem': 10.0}
    requests = [{'cpu': 2.25, 'mem': 3.5}, {'cpu': 3.00, 'mem': 6.0}]  # cpu total 5.25 leaves 0.25
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    resources = {'cpu': 5}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_capacity_raises():
    resources = {'cpu': -5}
    requests = [{'cpu': 0}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)
