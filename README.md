# RPC - Remote Procedure Call (Chamadas de Procedimento Remoto)

Este projeto (https://github.com/gabi-montenegro/RPC) implementa um sistema simples de RPC (Remote Procedure Call) em Python, permitindo que métodos de um serviço possam ser chamados remotamente por meio de sockets TCP, de maneira transparente para o cliente. Como exemplo prático, o projeto implementa uma calculadora que realiza as quatro operações básicas: adição, subtração, multiplicação e divisão.

## Introdução

RPC (Remote Procedure Call) é um mecanismo que permite que funções ou métodos sejam executados em outro processo ou máquina como se fossem chamadas locais. Neste projeto, o cliente realiza chamadas como `math_stub.add(5, 3)` e os parâmetros são enviados ao servidor, que executa o método correspondente e retorna o resultado. Nesse exemplo prático, cada operação matemática, ou seja cada método, vai executar em um servidor diferente.

O sistema é composto por:

- **Binder**: Responsável por manter um registro dos métodos disponíveis e os endereços dos servidores correspondentes.
- **Servidor RPC (`RPCServer`)**: Registra um método no binder e escuta requisições do cliente.
- **Cliente RPC (`RPCClient`)**: Busca o endereço do método no binder e envia a requisição.
- **Stub**: Gera dinamicamente chamadas remotas de forma transparente para o usuário.


## Estrutura do Projeto
```
RPC/
├── examples/
│ ├── server_example.py # Exemplo de servidor com múltiplos métodos de serviço implementados e solicitações de registro ao Binder.
│ └── client_example.py # Exemplo de cliente usando o stub
├── interface/
│ └── math_service.py # Assinatura dos métodos de serviço 'add', 'sub', 'multiply', 'divide'
├── rpc/
│ ├── rpc_binder.py # Servidor central que registra e resolve serviços
│ ├── rpc_server.py # Classe do servidor RPC
│ ├── rpc_client.py # Classe do cliente RPC
│ ├── rpc_stub_generator.py # Stub dinâmico
│ └── serializer.py # Serialização e desserialização com pickle
```

## Como executar

### Requisitos
1. Python (>= 3.7)

### Passo a Passo
1. Em um terminal, inicie o servidor do Binder. Por padrão, o binder é iniciado em localhost na porta 9000.

```bash
python rpc/rpc_binder.py
```

2. Em outro terminal, gere os stubs do servidor e do cliente.
```bash
python rpc/rpc_stub_generator.py
```

3. Com os stubs gerados, inicie o servidor RPC que vai registrar todos os métodos no binder. As portas dos serviços são definidas automaticamente a partir da porta base 5000, além do IP padrão definido como localhost.
```bash
python examples/server_example.py
```

4. Por fim, em outro terminal, execute o cliente.
```bash
python examples/client_examples.py
```

**OBS.:** Caso queria executar os servidores do Binder e dos serviços em outro IP, basta definir as variáveis de ambiente: BINDER_HOST e SERVICES_HOST. Exemplo:
```bash
export BINDER_HOST=<IP>
```

```bash
export SERVICES_HOST=<IP>
```

## Exemplo de execução

1. Com todos os métodos implementados e registrados (add, multiply, sub e divide) e com o seguinte bloco de execução no cliente (`examples/client_example.py`) que instancia o stub e acessa os métodos:
```python
from rpc.stub_client import Calculator

if __name__ == "__main__":
    math_stub = Calculator()
    
    print("Resultado de 5 + 3:", math_stub.add(5, 3))
    print("Resultado de 4 * 2:", math_stub.multiply(4, 2))
    print("Resultado de 5 - 3:", math_stub.sub(5, 3))
    print("Resultado de 4 / 2:", math_stub.divide(4, 2))

```

2. Executa-se o servidor do binder e os servidor RPC.
```bash
python rpc/rpc_binder.py
```

```bash
python examples/server_example.py
```

![](./image(1).png)


3. O programa do cliente é executado com:
```bash
python examples/client_example.py
```

![](./image(2).png)


## Inserção de novos serviços

1. Declare a assinatura do método do serviço na interface - classe `MathService` (arquivo `interface/math_service.py`) -  com os argumentos necessários. No exemplo, foi utilizado a inclusão do serviço de multiplicação.

```python
def multiply(a, b): pass 
```

2. Em seguida, no arquivo `examples/server_example.py` implemente o método do serviço na classe `MethodsService`. 

```python
def multiply(self, a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Argumentos de 'multiply' devem ser inteiros")
    return a * b
```

3. Ainda em `examples/server_example.py`, registre o novo serviço no método `start` da classe `MathRPCServer`:

```python
def start(self):
    print("[Server] Servidor RPC rodando. Pressione Ctrl+C para sair.")
    # Registrar métodos válidos da instância de serviço
    self.server.register(self.service.add)
    self.server.register(self.service.sub)
    self.server.register(self.service.multiply)
```

Obs.: O nome usado no `register()` deve ser exatamente o mesmo da assinatura definida na interface. Caso contrário, o cliente não conseguirá encontrar o serviço.


3. Sempre que a interface for modificada, é necessário regenerar os stubs para que o cliente reconheça o novo método:
```bash
python rpc/rpc_stub_generator.py
```

4. Execute o binder e o servidor RPC normalmente. O novo serviço agora estará disponível para os clientes.


## Validação de tipos dos argumentos
Os métodos dos serviços implementados na classe `MethodsService` (arquivo `examples/server_example.py`) verificam se os argumentos são inteiros. Caso argumentos inválidos sejam enviados, o erro é detectado no servidor e repassado ao cliente.

Exemplo de execução com a seguinte chamada:
```python
math_stub.add("x", 3)
```

Gera a saída ao cliente:
```bash
RuntimeError: Erro: Argumentos de 'add' devem ser inteiros
```

![](./image(4).png)


## Validação de métodos
Quando o cliente tenta chamar um método inexistente, como `math_stub.adds(1, 2)` (note o adds com "s" a mais), o `RPCClient` não encontra o método registrado no binder. Nesse caso, o erro ocorre ainda no lado do cliente, pois o binder não retorna um endereço válido para o método solicitado.

Exemplo de execução com a seguinte chamada:
```python
math_stub.adds(1, 2)
```

Gera a saída ao cliente:

```bash
AttributeError: Método 'adds' não existe na interface. Use: divide, add, sub, multiply
```

![](./image(5).png)

