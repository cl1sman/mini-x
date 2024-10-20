# Sistema de Mensagens UDP (Mini Twitter)

Este projeto implementa um sistema de mensagens UDP inspirado em um mini Twitter. Ele permite que múltiplos clientes enviem mensagens para outros clientes ou para todos os usuários conectados a um servidor.

## Estrutura do Sistema

O sistema consiste em dois componentes principais:
1. **Servidor UDP**: Gerencia os clientes conectados, distribui mensagens e envia mensagens periódicas para todos os clientes.
2. **Cliente UDP**: Conecta-se ao servidor, envia mensagens para outros clientes e recebe mensagens.

### Funcionalidades

- O servidor aceita conexões de clientes e retransmite mensagens entre eles.
- O cliente pode enviar mensagens para um destinatário específico ou para todos os clientes conectados.
- O servidor envia uma mensagem de broadcast a cada 60 segundos com informações sobre o número de clientes conectados.
- O cliente pode se desconectar enviando um comando `TCHAU`.
- O cliente detecta timeouts e tenta reconectar se não houver resposta do servidor.

## Requisitos

- Python 3.x
- Conexão de rede

## Como usar

### 1. Clonar o repositório

```bash
git clone https://github.com/cl1sman/mini-x.git
cd mini-x
```

### 2. Executar o servidor

O servidor deve ser iniciado primeiro. Ele escuta as conexões de clientes na porta 12345.

```bash
python3 server_udp.py
```

Você deve ver a seguinte saída ao iniciar o servidor:

```
[LOG] Servidor iniciado na porta 12345.
```

### 3. Executar o cliente

Inicie o cliente em uma outra janela de terminal ou em outra máquina. Cada cliente precisa de um ID e um nome único.

```bash
python3 client_udp.py
```

Ao iniciar, o cliente pedirá o IP do servidor, a porta e o ID do cliente. Exemplo de execução:

```
Digite o IP do servidor: 127.0.0.1
Digite a porta do servidor: 12345
Digite seu ID: 1
Digite seu nome: Alice
Mensagem 'OI' enviada ao servidor.
```

### 4. Enviar mensagens

Após a conexão com o servidor, o cliente pode enviar mensagens para um destinatário específico (pelo ID) ou enviar para todos os clientes conectados (ID 0 para todos).

Exemplo de envio de mensagem:

```
Digite o ID do destinatário (0 para todos): 2
Digite sua mensagem: Olá, cliente 2!
```

A mensagem será retransmitida para o cliente de ID 2.

### 5. **Encerrar o cliente**

Para desconectar um cliente, basta pressionar **Ctrl+C** no terminal onde o cliente está rodando. O cliente enviará uma mensagem `TCHAU` ao servidor e se desconectará corretamente. Exemplo de saída:

```
Encerrando conexão...
Mensagem 'TCHAU' enviada ao servidor.
```

### 6. **Encerrar o servidor**

O servidor pode ser encerrado manualmente utilizando **Ctrl+C** no terminal onde ele está rodando. Não há necessidade de enviar uma mensagem específica de encerramento, uma vez que o servidor não mantém estado crítico após o desligamento.

### 7. Logs do servidor

O servidor mantém logs de todas as atividades importantes, como conexões e desconexões de clientes. Exemplo de log:

```
[LOG] Cliente 1 (Alice) conectado.
[LOG] Cliente 2 (Bob) conectado.
[LOG] Cliente 1 desconectado.
```

## Configurações Adicionais

### Timeout do cliente

Por padrão, o timeout do cliente é configurado para **30 segundos**. Caso queira aumentar ou reduzir o tempo, basta alterar o valor da variável `TIMEOUT` no arquivo `client_udp.py`.

```python
TIMEOUT = 30  # Timeout ajustado para 30 segundos
```

O cliente exibirá a mensagem **"Timeout: Nenhuma resposta do servidor. Tentando novamente..."** se não receber uma resposta do servidor dentro desse período.

### Estrutura de Arquivos

- `server_udp.py`: Código do servidor UDP que gerencia as conexões e mensagens dos clientes.
- `client_udp.py`: Código do cliente UDP que se conecta ao servidor e envia mensagens.
- `README.md`: Este arquivo de instruções.

## Exemplo de uso

1. Inicie o **servidor**:
   ```bash
   python3 server_udp.py
   ```

2. Inicie dois **clientes** (em terminais diferentes ou máquinas diferentes):
   ```bash
   python3 client_udp.py
   ```
   Digite o IP do servidor e os dados do cliente conforme solicitado.

3. Envie mensagens entre os clientes ou envie uma mensagem para todos.
