import inspect
import importlib.util

class StubGenerator:
    def __init__(self, interface_path):
        self.interface_path = interface_path
        self.valid_methods = self.get_valid_methods()

    def get_valid_methods(self):
        spec = importlib.util.spec_from_file_location("interface", self.interface_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        valid_methods = []
        for class_name, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ == module.__name__:
                methods = [
                    name for name, member in inspect.getmembers(cls, inspect.isfunction)
                    if not name.startswith("__")
                ]
                valid_methods.extend(methods)

        return list(set(valid_methods))

    def generate_server_stub(self, output_file):
        stub_code = "from rpc.rpc_server import RPCServer\n"
        stub_code += "import os\n"
        stub_code += "from threading import Thread\n\n"
        stub_code += "class ServerStub:\n"
        stub_code += "    def __init__(self):\n"
        stub_code += "        self.rpc = RPCServer()\n"
        stub_code += "        self.port_counter = 5000\n"
        stub_code += "        self.services_host = os.getenv('SERVICES_HOST', 'localhost')\n"
        stub_code += f"        self.valid_methods = {self.valid_methods}  # Métodos da interface\n\n"

        stub_code += "    def register(self, impl_func):\n"
        stub_code += "        method_name = impl_func.__name__\n\n"
        stub_code += "        if method_name not in self.valid_methods:\n"
        stub_code += "            raise ValueError(\n"
        stub_code += "                f\"Método '{method_name}' não é válido para registro. \"\n"
        stub_code += "                f\"Métodos válidos: {', '.join(self.valid_methods)}\"\n"
        stub_code += "            )\n\n"
        stub_code += "        self.port_counter += 1\n"
        stub_code += "        port = self.port_counter\n\n"
        stub_code += "        if not self.rpc.register(method_name, self.services_host, port):\n"
        stub_code += "            print(f\"[ERRO] Falha ao registrar '{method_name}' no Binder\")\n"
        stub_code += "            return False\n\n"
        stub_code += "        Thread(target=self.rpc.handle_client, args=(port, impl_func), daemon=True).start()\n"
        stub_code += "        return True\n"
        stub_code += "    def stop(self):\n"
        stub_code += "        self.rpc.stop()\n"

        with open(output_file, 'w') as f:
            f.write(stub_code)

    def generate_client_stub(self, output_file):
        stub_code = "from rpc.rpc_client import RPCClient\n\n"
        stub_code += "class Calculator:\n"
        stub_code += "    def __init__(self):\n"
        stub_code += "        self.rpc = RPCClient()\n"
        stub_code += f"        self.valid_methods = {self.valid_methods}  # Métodos da interface\n\n"
        stub_code += "    def __getattr__(self, method_name):\n"
        stub_code += "        if method_name not in self.valid_methods:\n"
        stub_code += "            raise AttributeError(f\"Método '{method_name}' não existe na interface. Use: {', '.join(self.valid_methods)}\")\n\n"
        stub_code += "        def remote_call(*args):\n"
        stub_code += "            try:\n"
        stub_code += "                lookup_result = self.rpc.lookup(method_name)\n"
        stub_code += "                if not lookup_result:\n"
        stub_code += "                    raise RuntimeError(f\"Serviço '{method_name}' não encontrado\")\n\n"
        stub_code += "                ip, port = lookup_result\n"
        stub_code += "                return self.rpc.call(ip, port, *args)\n"
        stub_code += "            except ConnectionRefusedError:\n"
        stub_code += "                raise RuntimeError(f\"Serviço '{method_name}' indisponível\")\n"
        stub_code += "            except Exception as e:\n"
        stub_code += "                raise RuntimeError(f\"Erro: {str(e)}\")\n\n"
        stub_code += "        return remote_call\n"

        with open(output_file, 'w') as f:
            f.write(stub_code)


if __name__ == "__main__":
    generator = StubGenerator("interface/math_service.py")
    generator.generate_server_stub("rpc/stub_server.py")
    generator.generate_client_stub("rpc/stub_client.py")
