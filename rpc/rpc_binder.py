import socket
from threading import Thread

class Binder:
    def __init__(self, host="localhost", port=9000):
        self.services = {}
        self.host = host
        self.port = port

    def handle_client(self, conn):
        with conn:
            data = conn.recv(1024).decode()
            parts = data.split("|")
            if parts[0] == "REGISTER":
                _, method_name, ip, port = parts
                self.services[method_name] = (ip, int(port))
                conn.send(b"OK")
            elif parts[0] == "LOOKUP":
                _, method_name = parts
                result = self.services.get(method_name)
                if result:
                    conn.send(f"{result[0]}|{result[1]}".encode())
                else:
                    conn.send(b"NOT_FOUND")

    def start_binder(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen()
        print(f"[Binder] Escutando em {self.host}:{self.port}")
        while True:
            conn, _ = s.accept()
            Thread(target=self.handle_client, args=(conn,)).start()

if __name__ == "__main__":
    binder = Binder()
    binder.start_binder()
