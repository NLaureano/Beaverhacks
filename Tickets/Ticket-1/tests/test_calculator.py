from pathlib import Path
import sys

CODEBASE_DIR = Path(__file__).resolve().parent.parent / "Codebase"
sys.path.insert(0, str(CODEBASE_DIR))

from calculator import add, subtract, multiply, divide


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(3, 8) == -5


def test_multiply():
    assert multiply(6, 7) == 42
    assert multiply(-2, 5) == -10


def test_divide():
    assert divide(20, 5) == 4
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    try:
        divide(1, 0)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Cannot divide by zero"
