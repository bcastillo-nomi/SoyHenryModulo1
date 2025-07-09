class SaldoCuentaBancaria:

    def __init__(self, saldo_inicial):

        self.saldo = saldo_inicial


    def incrementar(self, monto):

        if not isinstance(monto, (int, float)) or monto != monto:  # Checking for NaN in Python

            raise ValueError("El monto debe ser un número válido")


        self.saldo += monto


    def resetear(self):

        self.saldo = 0


    def obtener_saldo(self):

        return self.saldo