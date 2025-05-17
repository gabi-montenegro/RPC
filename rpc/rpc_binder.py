import socket
from threading import Thread

class Binder:
    def __init__(self, host="localhost", port=9000):
        self.services = {}
        self.host = host
        self.port = port
        self.socket = None
        self.running = True

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
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"[Binder] Escutando em {self.host}:{self.port}")
        while self.running:
            try:
                conn, _ = self.socket.accept()
                Thread(target=self.handle_client, args=(conn,), daemon=True).start()
            except OSError:
                break  # Socket fechado

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()
            print("[Binder] Encerrado.")

if __name__ == "__main__":
    binder = Binder()
    t = Thread(target=binder.start_binder, daemon=True)
    t.start()

    print("[Binder] Digite \SAIR para encerrar o servidor.")
    try:
        while True:
            cmd = input()
            if cmd.strip() == "\SAIR":
                binder.stop()
                break
    except KeyboardInterrupt:
        binder.stop()
