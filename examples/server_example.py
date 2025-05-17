from threading import Thread
from rpc.rpc_server import RPCServer
from interface.math_service import MathService

if __name__ == "__main__":
    service = MathService()
    base_port = 5000

    # method_ports = {
    #     "add": 5000,
    #     "sub": 5001,
    #     "mul": 5002,
    # }
    methods = [method for method in dir(service) if not method.startswith("_") and callable(getattr(service, method))]

    threads = []
    servers = []

    

    for i, method in enumerate(methods):
        port = base_port + i
        server = RPCServer(method, service, port=port)
        servers.append(server)
        t = Thread(target=server.serve, daemon=True)  # roda em thread daemon
        t.start()
        threads.append(t)
        print(f"[Main] Servidor para '{method}' iniciado na porta {port}")

    print("[Main] Digite \SAIR para encerrar os servidores.")
    try:
        while True:
            cmd = input()
            if cmd.strip().upper() == "\SAIR":
                print("[Main] Encerrando servidores...")
                for s in servers:
                    s.close()  # certifique-se de que RPCServer tenha um método close()
                break
    except KeyboardInterrupt:
        print("[Main] Encerrando servidores...")
        for s in servers:
            s.close()
