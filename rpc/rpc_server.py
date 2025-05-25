# rpc_server.py
import socket
from threading import Thread
from .serializer import serialize, deserialize
import os

class RPCServer:
    def __init__(self, binder_host="localhost", binder_port=9000):
        self.binder = (binder_host, binder_port)
        self.servers = {}  # chave: porta, valor: socket
        self.services_host = os.getenv("SERVICES_HOST", "localhost")

    def register(self, name, ip, port):
        try:
            with socket.socket() as s:
                s.connect(self.binder)
                s.send(f"REGISTER|{name}|{ip}|{port}".encode())
                response = s.recv(1024).decode()
                return response == "OK"
        except (ConnectionRefusedError, OSError):
            print(f"[ERRO] Não foi possível conectar ao Binder em {self.binder[0]}:{self.binder[1]}")
            return False

    def handle_client(self, port, func):
        def client_handler(conn):
            with conn:
                try:
                    data = conn.recv(4096)
                    if not data:
                        return
                    args = deserialize(data)
                    result = func(*args)
                    conn.send(serialize(result))
                except Exception as e:
                    # print(f"[Server] Erro ao processar chamada: {e}")
                    conn.send(serialize({"error": str(e)}))

        s = socket.socket()
        s.bind((self.services_host, port))
        s.listen()
        self.servers[port] = s
        print(f"[Server] Método '{func.__name__}' escutando em  {self.services_host}:{port}")

        while True:
            try:
                conn, _ = s.accept()
                Thread(target=client_handler, args=(conn,), daemon=True).start()
            except OSError:
                # Socket foi fechado
                break

    def stop(self):
        print("[Server] Encerrando todos os sockets...")
        for port, sock in self.servers.items():
            try:
                sock.close()
                print(f"[Server] Socket da porta {port} fechado.")
            except Exception as e:
                print(f"[ERRO] Ao fechar socket da porta {port}: {e}")
