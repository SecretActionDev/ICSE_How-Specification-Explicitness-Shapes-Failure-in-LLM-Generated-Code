## Student Name: Rajendra Brahmbhatt
## Student ID: 217925157

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

# ======================= solution.py =======================

from typing import Dict, List, Union

Number = Union[int, float]

def is_allocation_feasible(
    resources: Dict[str, Number],
    requests: List[Dict[str, Number]]
) -> bool:
    """
    Determine whether a set of resource requests can be satisfied.

    New requirement:
    At least ONE resource must remain unallocated after assignment.
    If all resources are fully consumed → allocation is NOT feasible.
    """

    # capacities must be non-negative
    for capacity in resources.values():
        if capacity < 0:
            return False

    usage: Dict[str, Number] = {}

    for request in requests:
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")

        for resource, amount in request.items():
            if amount < 0:
                return False

            if resource not in resources:
                return False

            usage[resource] = usage.get(resource, 0) + amount

            # capacity exceeded
            if usage[resource] > resources[resource]:
                return False

    # ================= NEW CONSTRAINT =================
    # At least one resource must remain unallocated
    # i.e. exists resource where usage < capacity

    if not resources:
        # no resources exist -> trivially feasible
        return True

    for resource, capacity in resources.items():
        used = usage.get(resource, 0)
        if used < capacity:
            return True  # at least one leftover exists

    # if all resources exactly consumed
    return False


# ======================= test_solution.py =======================

import pytest
from solution import is_allocation_feasible

# ---------- BASIC FUNCTIONALITY ----------

def test_basic_valid_with_leftover():
    resources = {"cpu": 10}
    requests = [{"cpu": 3}, {"cpu": 4}]
    assert is_allocation_feasible(resources, requests) is True

def test_exceeds_capacity_invalid():
    resources = {"cpu": 5}
    requests = [{"cpu": 6}]
    assert is_allocation_feasible(resources, requests) is False

def test_missing_resource_invalid():
    resources = {"cpu": 5}
    requests = [{"gpu": 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_negative_request_invalid():
    resources = {"cpu": 5}
    requests = [{"cpu": -1}]
    assert is_allocation_feasible(resources, requests) is False

def test_negative_capacity_invalid():
    resources = {"cpu": -5}
    requests = [{"cpu": 1}]
    assert is_allocation_feasible(resources, requests) is False

def test_non_dict_request_raises():
    resources = {"cpu": 5}
    requests = [{"cpu": 1}, ["cpu", 2]]
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# ---------- NEW REQUIREMENT TESTS ----------

def test_all_resources_fully_consumed_invalid():
    resources = {"cpu": 10, "ram": 20}
    requests = [
        {"cpu": 5, "ram": 10},
        {"cpu": 5, "ram": 10}
    ]
    assert is_allocation_feasible(resources, requests) is False

def test_single_resource_exact_consumption_invalid():
    resources = {"cpu": 5}
    requests = [{"cpu": 5}]
    assert is_allocation_feasible(resources, requests) is False

def test_one_resource_leftover_valid():
    resources = {"cpu": 10, "ram": 20}
    requests = [{"cpu": 10, "ram": 5}]
    assert is_allocation_feasible(resources, requests) is True

def test_partial_consumption_valid():
    resources = {"cpu": 10}
    requests = [{"cpu": 9}]
    assert is_allocation_feasible(resources, requests) is True


# ---------- EDGE CASES ----------

def test_empty_requests_valid():
    resources = {"cpu": 10, "ram": 5}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_empty_resources_and_requests_valid():
    resources = {}
    requests = []
    assert is_allocation_feasible(resources, requests) is True

def test_zero_capacity_zero_request_invalid():
    resources = {"cpu": 0}
    requests = [{"cpu": 0}]
    # fully consumed (0 of 0) → no leftover
    assert is_allocation_feasible(resources, requests) is False

def test_zero_capacity_with_other_leftover_valid():
    resources = {"cpu": 0, "ram": 10}
    requests = [{"cpu": 0, "ram": 5}]
    # RAM still has leftover
    assert is_allocation_feasible(resources, requests) is True

def test_float_exact_consumption_invalid():
    resources = {"cpu": 10.5}
    requests = [{"cpu": 10.5}]
    assert is_allocation_feasible(resources, requests) is False

def test_float_with_leftover_valid():
    resources = {"cpu": 10.5}
    requests = [{"cpu": 10.4}]
    assert is_allocation_feasible(resources, requests) is True

def test_many_resources_one_leftover_valid():
    resources = {"cpu": 4, "ram": 6, "disk": 8}
    requests = [
        {"cpu": 4, "ram": 6, "disk": 7}
    ]
    # disk has leftover
    assert is_allocation_feasible(resources, requests) is True

def test_many_resources_all_exact_invalid():
    resources = {"cpu": 4, "ram": 6, "disk": 8}
    requests = [
        {"cpu": 4, "ram": 6, "disk": 8}
    ]
    assert is_allocation_feasible(resources, requests) is False

def test_large_numbers_valid():
    resources = {"cpu": 10**12}
    requests = [{"cpu": 10**11}]
    assert is_allocation_feasible(resources, requests) is True

def test_large_numbers_exact_invalid():
    resources = {"cpu": 10**12}
    requests = [{"cpu": 10**12}]
    assert is_allocation_feasible(resources, requests) is False


# ================= EXTRA EDGE & CONSTRAINT TESTS =================

def test_all_resources_unused_valid():
    # nothing allocated → everything leftover → valid
    resources = {"cpu": 10, "ram": 20}
    requests = []
    assert is_allocation_feasible(resources, requests) is True


def test_only_one_resource_fully_consumed_but_others_left_valid():
    resources = {"cpu": 5, "ram": 10, "disk": 20}
    requests = [{"cpu": 5}]
    # cpu fully consumed but ram/disk still free
    assert is_allocation_feasible(resources, requests) is True


def test_each_resource_has_small_leftover_valid():
    resources = {"cpu": 10, "ram": 10}
    requests = [{"cpu": 9, "ram": 9}]
    # both still have leftover
    assert is_allocation_feasible(resources, requests) is True


def test_all_resources_exactly_consumed_multiple_requests_invalid():
    resources = {"cpu": 6, "ram": 6}
    requests = [
        {"cpu": 3, "ram": 2},
        {"cpu": 3, "ram": 4}
    ]
    # both exactly consumed
    assert is_allocation_feasible(resources, requests) is False


def test_request_missing_some_resources_but_all_consumed_invalid():
    resources = {"cpu": 5, "ram": 5}
    requests = [
        {"cpu": 5},
        {"ram": 5}
    ]
    # both fully consumed → invalid
    assert is_allocation_feasible(resources, requests) is False


def test_resource_never_requested_counts_as_leftover_valid():
    resources = {"cpu": 5, "ram": 5, "disk": 10}
    requests = [{"cpu": 5, "ram": 5}]
    # disk unused → leftover exists
    assert is_allocation_feasible(resources, requests) is True


def test_usage_accumulation_across_many_requests_invalid():
    resources = {"cpu": 100}
    requests = [{"cpu": 25}, {"cpu": 25}, {"cpu": 25}, {"cpu": 25}]
    # exactly 100 used → invalid now
    assert is_allocation_feasible(resources, requests) is False


def test_usage_accumulation_many_requests_with_leftover_valid():
    resources = {"cpu": 100}
    requests = [{"cpu": 25}, {"cpu": 25}, {"cpu": 25}]
    # 75 used → leftover exists
    assert is_allocation_feasible(resources, requests) is True


def test_float_precision_edge_exact_invalid():
    resources = {"cpu": 1.0}
    requests = [{"cpu": 0.1}, {"cpu": 0.2}, {"cpu": 0.3}, {"cpu": 0.4}]
    # sums to 1.0 exactly → invalid
    assert is_allocation_feasible(resources, requests) is False


def test_float_precision_edge_leftover_valid():
    resources = {"cpu": 1.0}
    requests = [{"cpu": 0.1}, {"cpu": 0.2}, {"cpu": 0.3}]
    # 0.6 used → leftover exists
    assert is_allocation_feasible(resources, requests) is True


def test_very_small_leftover_valid():
    resources = {"cpu": 10}
    requests = [{"cpu": 9.999}]
    # tiny leftover still counts
    assert is_allocation_feasible(resources, requests) is True


def test_many_resources_only_last_has_leftover_valid():
    resources = {"cpu": 5, "ram": 5, "disk": 5}
    requests = [
        {"cpu": 5},
        {"ram": 5},
        {"disk": 4}
    ]
    # disk has leftover
    assert is_allocation_feasible(resources, requests) is True


def test_many_resources_all_but_one_exact_then_last_exact_invalid():
    resources = {"cpu": 5, "ram": 5, "disk": 5}
    requests = [
        {"cpu": 5},
        {"ram": 5},
        {"disk": 5}
    ]
    # all exact → invalid
    assert is_allocation_feasible(resources, requests) is False


def test_request_with_zero_amount_does_not_affect_leftover():
    resources = {"cpu": 5}
    requests = [{"cpu": 0}]
    # 5 still left
    assert is_allocation_feasible(resources, requests) is True


def test_multiple_zero_requests_invalid_if_capacity_zero():
    resources = {"cpu": 0}
    requests = [{"cpu": 0}, {"cpu": 0}]
    # fully consumed 0/0 → invalid by new rule
    assert is_allocation_feasible(resources, requests) is False


def test_large_scale_many_resources_mixed():
    resources = {
        "cpu": 1000,
        "ram": 2000,
        "disk": 5000,
        "net": 100
    }
    requests = [
        {"cpu": 1000},
        {"ram": 2000},
        {"disk": 4999},
        {"net": 100}
    ]
    # disk still has 1 leftover
    assert is_allocation_feasible(resources, requests) is True


def test_large_scale_all_exact_invalid():
    resources = {
        "cpu": 1000,
        "ram": 2000,
        "disk": 5000
    }
    requests = [
        {"cpu": 1000},
        {"ram": 2000},
        {"disk": 5000}
    ]
    # all fully consumed
    assert is_allocation_feasible(resources, requests) is False


def test_invalid_resource_type_inside_request():
    resources = {"cpu": 10}
    requests = [{"cpu": 5}, {"cpu": 3}, {"cpu": 2}, {"cpu": 0}]
    # exact consumption → invalid
    assert is_allocation_feasible(resources, requests) is False


def test_resource_with_never_used_and_zero_capacity_mix():
    resources = {"cpu": 5, "gpu": 0}
    requests = [{"cpu": 5}]
    # gpu fully consumed (0/0), cpu fully consumed → no leftover anywhere
    assert is_allocation_feasible(resources, requests) is False


def test_resource_with_never_used_positive_capacity_valid():
    resources = {"cpu": 5, "gpu": 10}
    requests = [{"cpu": 5}]
    # gpu unused → leftover exists
    assert is_allocation_feasible(resources, requests) is True
