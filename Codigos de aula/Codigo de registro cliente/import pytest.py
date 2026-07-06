import pytest 
from Calculadora import Calculadora

@pytest.fixture
def calc():
    return Calculadora()

def test_soma(calc):
    assert calc.soma(2, 3) == 5