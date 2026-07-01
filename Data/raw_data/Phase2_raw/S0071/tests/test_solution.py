## Student Name: Sanjay Raveendran
## Student ID: 217975467

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from solution import is_allocation_feasible

# ---------- BASIC FUNCTIONALITY ----------

def test_single_resource_under_capacity_is_feasible():
    resources = {"cpu": 10}
    requests = [{"cpu": 3}, {"cpu": 4}]
    assert is_allocation_feasible(resources, requests) is True


def test_single_resource_exactly_consumed_is_infeasible():
    resources = {"cpu": 10}
    requests = [{"cpu": 5}, {"cpu": 5}]
    assert is_allocation_feasible(resources, requests) is False


# ---------- MULTI-RESOURCE CASES ----------

def test_multi_resource_one_left_unallocated_is_feasible():
    resources = {"cpu": 8, "mem": 32}
    requests = [{"cpu": 4, "mem": 16}]
    assert is_allocation_feasible(resources, requests) is True


def test_multi_resource_all_exactly_consumed_is_infeasible():
    resources = {"cpu": 4, "mem": 8}
    requests = [{"cpu": 4, "mem": 8}]
    assert is_allocation_feasible(resources, requests) is False


def test_multi_resource_one_overloaded():
    resources = {"cpu": 8, "mem": 30}
    requests = [
        {"cpu": 2, "mem": 8},
        {"cpu": 3, "mem": 10},
        {"cpu": 3, "mem": 14},
    ]
    assert is_allocation_feasible(resources, requests) is False


# ---------- RESOURCE EXISTENCE ----------

def test_request_for_missing_resource_is_infeasible():
    resources = {"cpu": 10}
    requests = [{"cpu": 2}, {"gpu": 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_request_subset_of_resources_is_allowed():
    resources = {"cpu": 10, "mem": 32}
    requests = [{"cpu": 5}]
    assert is_allocation_feasible(resources, requests) is True


# ---------- STRUCTURAL VALIDATION ----------

def test_non_dict_request_raises_value_error():
    resources = {"cpu": 5}
    requests = [{"cpu": 2}, ["mem", 1]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


def test_all_requests_must_be_dicts():
    resources = {"cpu": 5}
    requests = [["cpu", 2]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# ---------- EDGE CASES ----------

def test_empty_requests_with_positive_resources_is_feasible():
    resources = {"cpu": 4, "mem": 16}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_empty_requests_with_zero_capacity_is_infeasible():
    resources = {"cpu": 0}
    requests = []
    assert is_allocation_feasible(resources, requests) is False


def test_zero_capacity_resource_requested_is_infeasible():
    resources = {"cpu": 0}
    requests = [{"cpu": 1}]
    assert is_allocation_feasible(resources, requests) is False


# ---------- CONSISTENCY / INVARIANTS ----------

def test_usage_accumulates_across_requests():
    resources = {"cpu": 10}
    requests = [{"cpu": 3}, {"cpu": 3}, {"cpu": 3}]
    assert is_allocation_feasible(resources, requests) is True


def test_order_of_requests_does_not_matter():
    resources = {"cpu": 6}
    requests1 = [{"cpu": 2}, {"cpu": 3}]
    requests2 = [{"cpu": 3}, {"cpu": 2}]
    assert is_allocation_feasible(resources, requests1) == is_allocation_feasible(resources, requests2)
