from solution import is_allocation_feasible
import pytest


def test_basic_feasible_single_resource_with_leftover():
    # Must leave leftover now
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 2}]  # total = 9, leftover = 1
    assert is_allocation_feasible(resources, requests) is True


def test_exactly_consumes_all_resources_is_now_infeasible():
    resources = {'cpu': 10}
    requests = [{'cpu': 3}, {'cpu': 4}, {'cpu': 3}]  # total = 10, leftover = 0
    assert is_allocation_feasible(resources, requests) is False


def test_multi_resource_infeasible_one_overloaded():
    resources = {'cpu': 8, 'mem': 30}
    requests = [{'cpu': 2, 'mem': 8}, {'cpu': 3, 'mem': 10}, {'cpu': 3, 'mem': 14}]
    assert is_allocation_feasible(resources, requests) is False


def test_missing_resource_in_availability():
    resources = {'cpu': 10}
    requests = [{'cpu': 2}, {'gpu': 1}]
    assert is_allocation_feasible(resources, requests) is False


def test_non_dict_request_raises():
    resources = {'cpu': 5}
    requests = [{'cpu': 2}, ['mem', 1]]  # malformed request
    with pytest.raises(ValueError):
        is_allocation_feasible(resources, requests)


# --- Additional tests for the new requirement (at least 5) ---

def test_multi_resource_leftover_on_one_resource_is_feasible():
    resources = {'cpu': 10, 'mem': 10}
    requests = [{'cpu': 10, 'mem': 9}]  # cpu leftover 0, mem leftover 1
    assert is_allocation_feasible(resources, requests) is True


def test_multi_resource_all_consumed_is_infeasible():
    resources = {'cpu': 10, 'mem': 10}
    requests = [{'cpu': 10, 'mem': 10}]  # leftover none
    assert is_allocation_feasible(resources, requests) is False


def test_no_requests_is_feasible_if_resources_exist():
    resources = {'cpu': 10}
    requests = []
    # leftover cpu = 10
    assert is_allocation_feasible(resources, requests) is True


def test_empty_resources_is_infeasible_even_with_no_requests():
    resources = {}
    requests = []
    assert is_allocation_feasible(resources, requests) is False


def test_leftover_requirement_blocks_exact_fit_even_if_within_capacity():
    resources = {'cpu': 5}
    requests = [{'cpu': 5}]
    assert is_allocation_feasible(resources, requests) is False
