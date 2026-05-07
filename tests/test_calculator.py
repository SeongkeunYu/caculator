import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


def test_tc001_add_integers(calc):
    assert calc.add(3, 5) == 8

def test_tc002_add_floats(calc):
    assert calc.add(1.5, 2.5) == 4.0

def test_tc003_subtract_integers(calc):
    assert calc.subtract(10, 3) == 7

def test_tc004_subtract_floats(calc):
    result = calc.subtract(0.5, 0.2)
    assert abs(result - 0.3) < 1e-9

def test_tc005_multiply_integers(calc):
    assert calc.multiply(4, 3) == 12

def test_tc006_multiply_floats(calc):
    assert calc.multiply(2.0, 3.0) == 6.0

def test_tc007_divide_integers(calc):
    assert calc.divide(10, 4) == 2.5

def test_tc008_divide_negative(calc):
    assert calc.divide(-9, 3) == -3.0

def test_tc009_add_zeros(calc):
    assert calc.add(0, 0) == 0

def test_tc010_multiply_by_zero(calc):
    assert calc.multiply(0, 999) == 0

def test_tc011_divide_zero_numerator(calc):
    assert calc.divide(0, 5) == 0.0

def test_tc012_subtract_negatives(calc):
    assert calc.subtract(-3, -1) == -2

def test_tc013_divide_by_zero(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(5, 0)

def test_tc014_add_string_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.add("a", 1)

def test_tc015_multiply_none_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.multiply(None, 2)

def test_tc016_divide_string_b_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.divide(1, "b")

def test_tc017_history_records_two_operations(calc):
    calc.add(1, 2)
    calc.subtract(5, 3)
    history = calc.get_history()
    assert len(history) == 2
    assert history[0] == {"operation": "add", "operands": [1, 2], "result": 3}
    assert history[1] == {"operation": "subtract", "operands": [5, 3], "result": 2}

def test_tc018_get_history_returns_copy(calc):
    calc.add(1, 2)
    history = calc.get_history()
    history.append({"operation": "fake", "operands": [], "result": 0})
    history[0]["result"] = 999
    assert len(calc.get_history()) == 1
    assert calc.get_history()[0]["result"] == 3

def test_tc022_history_records_divide_and_multiply(calc):
    calc.multiply(3, 4)
    calc.divide(10, 2)
    history = calc.get_history()
    assert history[0] == {"operation": "multiply", "operands": [3, 4], "result": 12}
    assert history[1] == {"operation": "divide", "operands": [10, 2], "result": 5.0}

def test_tc019_clear_history(calc):
    calc.add(1, 2)
    calc.clear_history()
    assert calc.get_history() == []

def test_tc020_reset_clears_history(calc):
    calc.multiply(3, 4)
    calc.reset()
    assert calc.get_history() == []

def test_tc021_subtract_string_raises_type_error(calc):
    with pytest.raises(TypeError):
        calc.subtract("x", 3)
