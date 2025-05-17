from rpc.rpc_stub_generator import Stub

if __name__ == "__main__":
    stub = Stub()
    print("Resultado de 5 + 3:", stub.add(5, 3))
    print("Resultado de 5 + 3:", stub.sub(1, 3))
    print("Resultado de 5 + 3:", stub.sub(1, 4))