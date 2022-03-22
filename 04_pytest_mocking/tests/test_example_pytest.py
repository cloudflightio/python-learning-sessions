import pytest

import src.db
import src.example
from src.example import foo
from src.example import multiply_with_constant


# mocker is a fixture from pytest-mock, which is a thin-wrapper around
# the patching api of the unittest.mock package
def test_example_pytest(mocker):
    mocker.patch(  # doesn't require that we import the object before patching
        # db_write is from db.py but imported into example.py
        'src.example.db_write',
        return_value=10
    )
    # db_write will be a MagicMock

    expected = 10
    actual = foo()
    assert expected == actual


# equivalent to
def test_example_pytest3(mocker):
    mocker.patch.object(  # requires that we import before patching
        # db_write is from db.py but imported into example.py
        src.example,
        "db_write",
        return_value=8  # specify directly the return value of mock
    )

    expected = 8
    actual = src.example.foo()
    assert expected == actual


# equivalent to
def test_example_pytest2(mocker):
    def mocked_dbwrite():
        # extra computations here
        return 9

    mocker.patch.object(
        # db_write is from db.py but imported into example.py
        src.example,
        "db_write",
        new=mocked_dbwrite  # if we need more than the return value
    )

    expected = 9
    actual = src.example.foo()
    assert expected == actual


def test_example_pytest_longrunning(mocker):
    def mocked_long_running_function():
        return {"status": 500}

    mocker.patch.object(
        src.example,
        "long_api_call",
        new=mocked_long_running_function
    )

    expected = 500
    actual = src.example.check_status()
    assert expected == actual

def test_compute(monkeypatch):
    monkeypatch.setattr("src.example.MY_CONSTANT", 3)
    assert multiply_with_constant(6) == 18


def test_floats_comparison_approx_abs():
    """
    Fails with:
    Expected :0.004 ± 1.0e-04
    Actual   :0.005
    because valid ranges are (0.0039 -> 0.0041)
    """
    assert 0.005 == pytest.approx(0.004, abs=1e-4)

    assert 0.004099999 == pytest.approx(0.004, abs=1e-4)  # passes
    assert 0.0041 == pytest.approx(0.004, abs=1e-4)       # fails

    assert 0.003900001 == pytest.approx(0.004, abs=1e-4)  # passes
    assert 0.0039 == pytest.approx(0.004, abs=1e-4)       # fails

def test_floats_comparison_approx_rel(): 
    """
    Fails with:
    Expected :0.004 ± 4.0e-06
    Actual   :0.005
    because rel uses 0.004 * 0.001 = 0.000004 = 4.0e-06 as a tolerance,
    valid ranges are 0.003996 -> 0.004004
    """
    # assert 0.005 == pytest.approx(0.004, rel=1e-3)
    assert 0.003996 == pytest.approx(0.004, rel=1e-3)
    assert 0.004004 == pytest.approx(0.004, rel=1e-3)

    assert 0.004002 == pytest.approx(0.004, rel=1e-4)  #passes


def test_list():
    assert (1, 2, 3) == (3, 2, 1)
