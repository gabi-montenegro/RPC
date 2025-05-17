from rpc.rpc_stub_generator import MathStub

if __name__ == "__main__":
    math_stub = MathStub()
    print("Resultado de 5 + 3:", math_stub.add(5, 3))