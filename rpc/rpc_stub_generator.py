from .rpc_client import RPCClient

class MathStub:
    def __init__(self):
        self.client = RPCClient("math_service") # localizacao do servico

    def add(self, a, b):
        return self.client.call("add", a, b) # chama o metodo do servico