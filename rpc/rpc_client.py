import socket
from .serializer import serialize, deserialize

class RPCClient:
    def __init__(self, method_name, binder_host="localhost", binder_port=9000):
        self.method_name = method_name
        self.binder_host = binder_host
        self.binder_port = binder_port
        self.service_addr = self.lookup_method()

    def lookup_method(self):
        with socket.socket() as s:
            s.connect((self.binder_host, self.binder_port))
            s.send(f"LOOKUP|{self.method_name}".encode())
            data = s.recv(1024).decode()
            if data == "NOT_FOUND":
                raise Exception(f"Método '{self.method_name}' não encontrado")
            ip, port = data.split("|")
            return (ip, int(port))

    def call(self, *args):
        with socket.socket() as s:
            s.connect(self.service_addr)
            s.send(serialize(args))
            result = s.recv(4096)
            return deserialize(result)
