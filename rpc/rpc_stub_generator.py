from .rpc_client import RPCClient
import socket

class Stub:
    def __getattr__(self, method_name):
        def remote_call(*args):
            try:
                client = RPCClient(method_name)
                return client.call(*args)
            except (ConnectionRefusedError):
                raise RuntimeError(f"[Stub] Erro: servidor RPC para '{method_name}' está indisponível.")
                
        return remote_call
