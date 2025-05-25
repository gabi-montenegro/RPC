import socket
from .serializer import serialize, deserialize
import os

class RPCClient:
    def __init__(self, binder_port=9000):
        self.binder = (os.getenv("BINDER_HOST", "localhost"), binder_port)

    def lookup(self, name):
        try:
            with socket.socket() as s:
                s.connect(self.binder)
                s.send(f"LOOKUP|{name}".encode())
                data = s.recv(1024).decode()
                if data == "NOT_FOUND":
                    print(f"Serviço '{name}' não encontrado no Binder")
                ip, port = data.split("|")
                return ip, int(port)
        except (ConnectionRefusedError, OSError):
            print(f"[ERRO] Não foi possível conectar ao Binder em {self.binder[0]}:{self.binder[1]}")
            return False

    def call(self, ip, port, *args):
        try:
            with socket.socket() as s:
                s.connect((ip, port))
                s.send(serialize(args))
                response = deserialize(s.recv(4096))
                if isinstance(response, dict) and "error" in response:
                    raise RuntimeError(response["error"])
                return response
        except ConnectionRefusedError:
            print(f"[ERRO] Não foi possível conectar ao servidor em {ip}:{port}")
            raise
