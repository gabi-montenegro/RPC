# RPC - Remote Procedure Call (Chamadas de Procedimento Remoto)

Este projeto implementa um sistema simples de RPC (Remote Procedure Call) em Python, permitindo que métodos de um serviço possam ser chamados remotamente por meio de sockets TCP, de maneira transparente para o cliente. Como exemplo prático, o projeto implementa uma calculadora que realiza as quatro operações básicas: adição, subtração, multiplicação e divisão.

## Introdução

RPC (Remote Procedure Call) é um mecanismo que permite que funções ou métodos sejam executados em outro processo ou máquina como se fossem chamadas locais. Neste projeto, o cliente realiza chamadas como `stub.add(5, 3)` e os parâmetros são enviados ao servidor, que executa o método correspondente e retorna o resultado.

O sistema é composto por:

- **Binder**: Responsável por manter um registro dos métodos disponíveis e os endereços dos servidores correspondentes.
- **Servidor RPC (`RPCServer`)**: Registra um método no binder e escuta requisições do cliente.
- **Cliente RPC (`RPCClient`)**: Busca o endereço do método no binder e envia a requisição.
- **Stub**: Gera dinamicamente chamadas remotas de forma transparente para o usuário.

---

## Estrutura do Projeto
RPC/
├── examples/
│ ├── server_example.py # Exemplo de servidor com múltiplos métodos
│ └── client_example.py # Exemplo de cliente usando o stub
├── interface/
│ └── math_service.py # Implementação dos métodos 'add', 'sub', 'mul', 'div'
├── rpc/
│ ├── binder.py # Servidor central que registra e resolve serviços
│ ├── rpc_server.py # Classe do servidor RPC
│ ├── rpc_client.py # Classe do cliente RPC
│ ├── rpc_stub_generator.py # Stub dinâmico
│ └── serializer.py # Serialização e desserialização com pickle


## Como executar

### Requisitos
1. Python (>= 3.7)

### Passo a Passo
1. Em um terminal, inicie o servidor do Binder. Por padrão, o binder é iniciado na porta 9000.

```bash
python rpc_binder.py
```

2. Em outro terminal, inicie os servidores dos métodos. As portas dos métodos são definidas no dicionário `method_ports` do `arquivo examples/server_examples.py`.
```bash
python examples/server_examples.py
```

3. Por fim, em outro terminal, execute o cliente.
```bash
python examples/client_examples.py
```

**OBS.:** Para sair dos servidores (binder e servidores dos métodos) basta digitar "\SAIR" no terminal.

## Exemplo de execução




## Inserção de novos serviços à biblioteca MathService
1. Insira o método do serviço na classe `MathService` (arquivo `interface/math_service.py`). No exemplo, foi utilizado a adição do serviço de multiplicação.
```python
def mul(self, a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Argumentos de 'mul' devem ser inteiros")
    return a * b
```
2. Em seguida, registre o nome do serviço (com o nome exato do método) e uma porta no dicionário `method_ports` do `arquivo examples/server_examples.py`.
```python
method_ports = {
    "add": 5000,
    "sub": 5001,
    "mul": 5002,
}
```
3. Para utilizar o serviço no cliente, basta acessá-lo com `stub.mul(1,4)` no arquivo `examples/client_example.py`.
```python
print("Resultado de 5 + 3:", stub.sub(1, 4))
```

4. Execute todos os servidores conforme no tópico "Como executar".

## Validação de tipos dos argumentos
Os métodos implementados na classe `MathService` (arquivo `interface/math_service.py`) verificam se os argumentos são inteiros. Caso argumentos inválidos sejam enviados, o erro é tratado no servidor e repassado ao cliente.

Exemplo de execução com a seguinte chamada:
```python
stub.add("x", 3)
```

Gera a saída ao cliente:

```
RuntimeError: [RPCClient] Erro do servidor: Argumentos de 'add' devem ser inteiros
```

[imagem]

## Validação de métodos
Quando o cliente tenta chamar um método inexistente, como `stub.adds(1, 2)` (note o adds com "s" a mais), o `RPCClient` não encontra o método registrado no binder. Nesse caso, o erro ocorre ainda no lado do cliente, pois o binder não retorna um endereço válido para o método solicitado.

Exemplo de execução com a seguinte chamada:
```python
stub.adds(1, 2)
```

Gera a saída ao cliente:

```
ValueError: [RPCClient] Método 'adds' não encontrado no binder
```

[imagem]