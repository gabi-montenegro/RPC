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
        self.socket = None

    def handle_client(self, conn):
        with conn:
            try:
                data = conn.recv(4096)
                args = deserialize(data)
                method = getattr(self.method_impl, self.method_name)
                result = method(*args)
                conn.send(serialize(result))
            except Exception as e:
                print(f"[RPCServer] Erro ao processar chamada: {e}")
                conn.send(serialize({"error": str(e)}))


    def serve(self):
        # Registra no binder
        try:
            with socket.socket() as b:
                b.connect(self.binder)
                b.send(f"REGISTER|{self.method_name}|{self.host}|{self.port}".encode())
                print(f"[RPCServer] Registrado '{self.method_name}' no binder")
        except ConnectionRefusedError:
            print(f"[RPCServer] ERRO: Não foi possível conectar ao binder em {self.binder[0]}:{self.binder[1]}")
            return

        # Cria socket para escutar chamadas
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"[RPCServer] Método '{self.method_name}' escutando em {self.host}:{self.port}")
        while True:
            conn, _ = self.socket.accept()
            Thread(target=self.handle_client, args=(conn,)).start()

    def close(self):
        if self.socket:
            print(f"[RPCServer] Fechando socket para o método '{self.method_name}'")
            self.socket.close()
