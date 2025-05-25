from rpc.stub_server import ServerStub
import time

class MethodsService:
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


class MathRPCServer:
    def __init__(self):
        self.server = ServerStub()
        self.service = MethodsService()

    def start(self):
        print("[Server] Servidor RPC rodando. Pressione Ctrl+C para sair.")
        # Registrar métodos válidos da instância de serviço
        self.server.register(self.service.add)
        self.server.register(self.service.sub)
        self.server.register(self.service.multiply)
        self.server.register(self.service.divide)

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\n[Server] Encerrando servidor.")
            self.server.stop()


if __name__ == "__main__":
    rpc_server = MathRPCServer()
    rpc_server.start()
