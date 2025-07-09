import pytest
from cuentaBancaria import SaldoCuentaBancaria

def test_saldo_inicial():
    cuenta = SaldoCuentaBancaria(100)
    assert cuenta.obtener_saldo() == 100

def test_incrementar_saldo():
    cuenta = SaldoCuentaBancaria(50)
    cuenta.incrementar(25)
    assert cuenta.obtener_saldo() == 75

def test_incrementar_saldo_float():
    cuenta = SaldoCuentaBancaria(10.5)
    cuenta.incrementar(4.5)
    assert cuenta.obtener_saldo() == 15.0

def test_incrementar_valor_invalido_str():
    cuenta = SaldoCuentaBancaria(0)
    with pytest.raises(ValueError):
        cuenta.incrementar("100")

def test_incrementar_valor_invalido_nan():
    cuenta = SaldoCuentaBancaria(0)
    nan = float('nan')
    with pytest.raises(ValueError):
        cuenta.incrementar(nan)

def test_resetear_saldo():
    cuenta = SaldoCuentaBancaria(200)
    cuenta.incrementar(50)
    cuenta.resetear()
    assert cuenta.obtener_saldo() == 0

def test_incrementar_valor_negativo():
    cuenta = SaldoCuentaBancaria(100)
    cuenta.incrementar(-30)
    assert cuenta.obtener_saldo() == 70