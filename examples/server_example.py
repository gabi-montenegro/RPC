from rpc.rpc_server import RPCServer
from interface.math_service import MathService

if __name__ == "__main__":
    service = MathService()
    server = RPCServer("math_service", service)
    # Cria socket e Registra o servico no binder
    print(dir(server))
    server.serve()