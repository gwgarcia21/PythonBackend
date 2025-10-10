import pytest
from .my_module import add

def test_add_positive_numbers():
  """Tests that add() returns the correct sum for positive numbers."""
  assert add(2, 3) == 5

def test_add_negative_numbers():
  """Tests that add() returns the correct sum for negative numbers."""
  assert add(-2, -3) == -5

def test_add_mixed_numbers():
  """Tests that add() returns the correct sum for mixed positive and negative numbers."""
  assert add(2, -3) == -1

def test_add_zero():
    """Tests that add() returns the correct sum when one number is zero."""
    assert add(5, 0) == 5