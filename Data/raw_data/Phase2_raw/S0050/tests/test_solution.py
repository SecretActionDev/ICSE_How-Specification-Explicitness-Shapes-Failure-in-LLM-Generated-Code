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
def test_empty_requests_is_feasible():
    # No requests means nothing to allocate -> feasible
    resources = {'cpu': 5, 'mem': 10}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_exact_capacity_is_feasible():
    # Total demand equals capacity -> feasible
    resources = {'cpu': 10}
    requests = [{'cpu': 6}, {'cpu': 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_negative_request_amount_raises():
    # Negative demand is invalid -> should raise
    resources = {'cpu': 10}
    requests = [{'cpu': -1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_negative_resource_capacity_raises():
    # Negative capacity is invalid -> should raise
    resources = {'cpu': -10}
    requests = [{'cpu': 1}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_request_value_non_numeric_raises():
    # Non-numeric demand is invalid -> should raise
    resources = {'cpu': 10}
    requests = [{'cpu': "3"}]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_float_amounts_feasible():
    # Supports floats; totals within capacity -> feasible
    resources = {'cpu': 5.0}
    requests = [{'cpu': 1.5}, {'cpu': 2.0}, {'cpu': 1.5}]
    assert is_allocation_feasible(resources, requests) is True


def test_request_missing_some_resources_ok():
    # Request can omit resources; missing treated as 0
    resources = {'cpu': 4, 'mem': 8}
    requests = [{'cpu': 2}, {'mem': 3}]
    assert is_allocation_feasible(resources, requests) is True