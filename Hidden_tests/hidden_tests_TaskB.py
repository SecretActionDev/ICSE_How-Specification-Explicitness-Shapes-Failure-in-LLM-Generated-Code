import pytest
from solution import is_allocation_feasible


# ------------------------
# VALUE ERRORS (INVALID NUMERIC VALUES)
# ------------------------
# CO
def test_TC1_negative_resource_value():
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": -1}, [{"cpu": 1}])
# CO
def test_TC2_negative_request_value():
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": -5}])
# CO
def test_TC3_nan_value():
    import math
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": math.nan}, [{"cpu": 1}])
# CO
def test_TC4_infinite_value():
    import math
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": math.inf}, [{"cpu": 1}])


# ------------------------
# TYPE ERRORS
# ------------------------
# AI
def test_TC5_resources_not_dict():
    with pytest.raises(TypeError):
        is_allocation_feasible(10, [{"cpu": 1}])
# CO
def test_TC6_requests_not_list():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, "invalid")
# AI
def test_TC7_request_item_not_dict():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, [5])
#AI
def test_TC8_resource_value_not_number():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": "ten"}, [{"cpu": 5}])
# AI
def test_TC9_request_value_not_number():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": "five"}])
# AI
def test_TC10_resource_key_not_string():
    with pytest.raises(TypeError):
        is_allocation_feasible({1: 10}, [{"cpu": 5}])
# AI
def test_TC11_request_key_not_string():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, [{1: 5}])


# ------------------------
# STRUCTURE ERRORS
# ------------------------
# IV
def test_TC12_missing_resource_type():
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": 5, "ram": 2}])
# IV
def test_TC13_empty_resource_dict_invalid():
    with pytest.raises(ValueError):
        is_allocation_feasible({}, [{"cpu": 1}])
# IV
def test_TC14_none_resources():
    with pytest.raises(TypeError):
        is_allocation_feasible(None, [{"cpu": 1}])
# CO
def test_TC15_none_requests():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, None)


# ------------------------
# EDGE INVALID STRUCTURES
# ------------------------
# CO
def test_TC16_nested_invalid_request():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": {"nested": 5}}])

#AI
def test_TC17_list_inside_request_value():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": [5]}])
# AI
def test_TC18_tuple_inside_request_value():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": (5,)}])


# ------------------------
# VALID CASES
# ------------------------
# CO
def test_TC19_valid_simple_case():
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": 5}]) is True

#CO
def test_TC20_valid_multi_resource():
    assert is_allocation_feasible(
        {"cpu": 10, "ram": 10},
        [{"cpu": 5, "ram": 5}]
    ) is True


# ------------------------
# MIXED EDGE + ERROR CASES
# ------------------------
# EC
def test_TC21_zero_and_negative_mix():
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 0}, [{"cpu": -1}])
# EC
def test_TC22_valid_zero_values():
    # Not feasible because resource=0, must leave 1 unit unallocated
    assert is_allocation_feasible({"cpu": 0}, [{"cpu": 0}]) is False
# IV
def test_TC23_request_with_extra_invalid_key():
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": 5, "gpu": 1}])


# ------------------------
# LARGE/BOOLEAN/STRING INVALID CASES
# ------------------------

# constrain
def test_TC24_string_number():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": "10"}, [{"cpu": 5}])
# CO
def test_TC25_string_number_in_request():
    with pytest.raises(TypeError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": "5"}])


# ------------------------
# EMPTY / FLOAT / DEEP EDGE CASES
# ------------------------
# EC
def test_TC26_empty_requests_valid():
    assert is_allocation_feasible({"cpu": 10}, []) is True
# EC
def test_TC27_empty_requests_invalid_resources():
    with pytest.raises(ValueError):
        is_allocation_feasible({}, [])
# AI
def test_TC28_valid_float():
    assert is_allocation_feasible({"cpu": 10.5}, [{"cpu": 5.5}]) is True
# CO
def test_TC29_invalid_float_nan_request():
    import math
    with pytest.raises(ValueError):
        is_allocation_feasible({"cpu": 10}, [{"cpu": math.nan}])


# ------------------------
# ONE RESOURCE MUST REMAIN UNALLOCATED
# (Merged into valid/edge cases to keep 33 total)
# ------------------------
def test_TC30_one_resource_must_remain_false():
    # exact allocation fails CO
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": 10}]) is False
   

def test_TC31_one_resource_must_remain_true():
    # leaving one unit free passes EC
    assert is_allocation_feasible({"cpu": 10}, [{"cpu": 9}]) is True

# EC
def test_TC32_multi_resource_exact_cpu():
    assert is_allocation_feasible(
        {"cpu": 10, "ram": 8},
        [{"cpu": 10, "ram": 5}]
    ) is True

# CO
def test_TC33_multi_resource_exact_cpu():
    assert is_allocation_feasible(
        {"cpu": 10, "ram": 8},
        [{"cpu": 10, "ram": 8}]
    ) is False
