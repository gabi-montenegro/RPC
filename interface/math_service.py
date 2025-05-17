class MathService:
    def add(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Argumentos de 'add' devem ser inteiros")
        return a + b

    def sub(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Argumentos de 'sub' devem ser inteiros")
        return a - b

    def multiply(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Argumentos de 'multiply' devem ser inteiros")
        return a * b

    def divide(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Argumentos de 'divide' devem ser inteiros")
        if b == 0:
            raise ValueError("Divisão por zero não é permitida")
        return a / b
