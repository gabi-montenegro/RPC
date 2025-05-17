import socket
from threading import Thread
from rpc.serializer import serialize, deserialize 


class RPCServer:
    def __init__(self, method_name, method_impl, host="localhost", port=5000, binder_host="localhost", binder_port=9000):
        self.method_name = method_name
        self.method_impl = method_impl
        self.host = host
        self.port = port
        self.binder = (binder_host, binder_port)

    def handle_client(self, conn):
        with conn:
            data = conn.recv(4096)
            args = deserialize(data)
            result = getattr(self.method_impl, self.method_name)(*args)
            conn.send(serialize(result))

    def serve(self):
        # Registra no binder
        with socket.socket() as b:
            b.connect(self.binder)
            b.send(f"REGISTER|{self.method_name}|{self.host}|{self.port}".encode())
            print(f"[RPCServer] Registrado '{self.method_name}' no binder")

        # Cria socket para escutar chamadas
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen()
        print(f"[RPCServer] Método '{self.method_name}' escutando em {self.host}:{self.port}")
        while True:
            conn, _ = s.accept()
            Thread(target=self.handle_client, args=(conn,)).start()
