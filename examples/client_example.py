from rpc.rpc_stub_generator import Stub

if __name__ == "__main__":
    math_stub = Stub()
    print("Resultado de 5 + 3:", math_stub.add(5, 3))
    print("Resultado de 5 + 3:", math_stub.sub(5, 3))