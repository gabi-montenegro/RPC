from .rpc_client import RPCClient

class Stub:
    def __getattr__(self, method_name):
        def remote_call(*args):
            client = RPCClient(method_name)
            return client.call(*args)
        return remote_call
