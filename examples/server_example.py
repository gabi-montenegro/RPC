from threading import Thread
from rpc.rpc_server import RPCServer
from interface.math_service import MathService

if __name__ == "__main__":
    service = MathService()

    method_ports = {
        "add": 5000,
        "sub": 5001,
    }

    threads = []

    for method, port in method_ports.items():
        server = RPCServer(method, service, port=port)
        t = Thread(target=server.serve, daemon=True)  # roda em thread daemon
        t.start()
        threads.append(t)
        print(f"[Main] Servidor para '{method}' iniciado na porta {port}")

    # Mantém o programa rodando para as threads não encerrarem
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[Main] Encerrando servidores...")
