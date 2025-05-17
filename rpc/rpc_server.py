import socket
from threading import Thread
from rpc.serializer import serialize, deserialize


class RPCServer(Thread):
    def __init__(self, service_name, service_impl, host="localhost", port=8000, binder_host="localhost", binder_port=9000):
        self.service_name = service_name # localizacao do servico (math_service)
        self.service_impl = service_impl # o modulo do servico acima que implementa as funcoes
        self.host = host
        self.port = port
        self.binder = (binder_host, binder_port)

    def handle_client(self, conn):
        with conn:
            data = conn.recv(4096)
            method_name, args = deserialize(data)
            result = getattr(self.service_impl, method_name)(*args)
            conn.send(serialize(result))

    def serve(self):
        # Cria o socket para escutar conexoes
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen()
        # Registra no binder
        with socket.socket() as b:
            b.connect(self.binder)
            b.send(f"REGISTER|{self.service_name}|{self.host}|{self.port}".encode())
            print(f"[RPCServer] Registrado no Binder como '{self.service_name}'")

        print(f"[RPCServer] Servidor '{self.service_name}' escutando em {self.host}:{self.port}")
        # Atende conexoes em uma nova thread
        while True:
            conn, _ = s.accept()
            Thread(target=self.handle_client, args=(conn,)).start()

        