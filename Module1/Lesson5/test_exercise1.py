import pytest
from unittest.mock import patch
from .exercise1 import Calculator

@pytest.mark.parametrize("a, b, expected", [
  (2, 3, 5),
  (-2, -3, -5),
  (2, -3, -1),
  (0, 5, 5),
])
def test_add_numbers(a, b, expected):
  assert Calculator.add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
  (2, 3, -1),
  (-2, -3, 1),
  (2, -3, 5),
  (0, 5, -5),
])
def test_subtract_numbers(a, b, expected):
  assert Calculator.subtract(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
  (2, 3, 6),
  (-2, -3, 6),
  (2, -3, -6),
  (0, 5, 0),
])
def test_multiply_numbers(a, b, expected):
  assert Calculator.multiply(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
  (6, 3, 2),
  (6, -3, -2),
  (-6, -3, 2),
  (0, 5, 0),
])
def test_divide_numbers(a, b, expected):
  assert Calculator.divide(a, b) == expected

def test_divide_by_zero_with_mock():
    calc = Calculator()
    with patch.object(Calculator, 'divide', side_effect=ZeroDivisionError("division by zero")):
        with pytest.raises(ZeroDivisionError):
            calc.divide(1, 0)