import socket
from .serializer import serialize, deserialize

class RPCClient:
    def __init__(self, service_name, binder_host="localhost", binder_port=9000):
        self.service_name = service_name # localizacao do servico (math_service)
        self.binder_host = binder_host
        self.binder_port = binder_port
        self.service_addr = self.lookup_service()

    def lookup_service(self):
        # Busca o endereco do servico
        with socket.socket() as s:
            s.connect((self.binder_host, self.binder_port))
            s.send(f"LOOKUP|{self.service_name}".encode())
            data = s.recv(1024).decode()
            if data == "NOT_FOUND":
                raise Exception("Serviço não encontrado")
            ip, port = data.split("|")
            return (ip, int(port))

    def call(self, method_name, *args):
        # Chama o servico passando os argumentos ("add", 5, 3)
        with socket.socket() as s:
            s.connect(self.service_addr)
            s.send(serialize((method_name, args)))
            result = s.recv(4096)
            return deserialize(result) # recebe resultado da funcao executada