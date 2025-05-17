class MathService:
    def add(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Argumentos de 'add' devem ser inteiros")
        return a + b

    def sub(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Argumentos de 'sub' devem ser inteiros")
        return a - b

    def mul(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("Argumentos de 'mul' devem ser inteiros")
        return a * b
