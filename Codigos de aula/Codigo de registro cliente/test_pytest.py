import pytest
from testcalcu import Calculadora

@pytest.fixture
def calcu():
    return Calculadora()

def test_soma(calcu):
    assert calcu.soma(2, 3) == 5
    
def test_subtracao(calcu):
        assert calcu.subtracao(10, 4) == 6
        
def test_multiplicacao(calcu):
        assert calcu.multiplicacao(3, 5) == 15
        
def test_divisao(calcu):
        assert calcu.divisao(10, 2) == 5

def test_divisao_por_zero(calcu):
        with pytest.raises(ValueError):
            calcu.divisao(10, 0)