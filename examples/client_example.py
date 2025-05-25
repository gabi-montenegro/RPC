from rpc.stub_client import Calculator

if __name__ == "__main__":
    math_stub = Calculator()
    
    print("Resultado de 5 + 3:", math_stub.add("x", 3))
    print("Resultado de 4 * 2:", math_stub.multiply(4, 2))
    print("Resultado de 5 - 3:", math_stub.sub(5, 3))
    print("Resultado de 4 / 2:", math_stub.divide(4, 2))