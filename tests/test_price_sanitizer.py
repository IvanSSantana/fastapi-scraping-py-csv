from utils import price_sanitizer
from decimal import Decimal, InvalidOperation
import pytest

def test_should_remove_rs():
    assert price_sanitizer("R$ 1900,50") == Decimal(1900.5)

def test_should_remove_dot():
    assert price_sanitizer("5.000.300,75") == Decimal(5000300.75)

def test_should_remove_percent():
    assert price_sanitizer("50%") == Decimal(50)

def test_should_raise_InvalidOperationException_for_not_numbers():
    fail_value = "Olá máquina!"

    with pytest.raises(InvalidOperation) as error:
        price_sanitizer(fail_value)

    assert str(error.value) == f"Error during conversion of {fail_value} to decimal."
    assert error.type == InvalidOperation
    