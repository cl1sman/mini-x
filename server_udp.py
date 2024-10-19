import socket
import threading
import time
from struct import pack, unpack

MSG_FORMAT = "iiii20s140s"
SERVER_ID = 0
clients = {}  # Dicionário para armazenar clientes conectados (ID -> Endereço)
log_lock = threading.Lock()

def log(message):
    with log_lock:
        print(f"[LOG] {message}")

def handle_client(data, address, server_socket):
    try:
        msg_type, origin_id, dest_id, msg_len, name, msg = unpack(MSG_FORMAT, data)
    except Exception as e:
        log(f"Mensagem malformada de {address}. Erro: {e}")
        return

    if msg_type == 0:  # OI (mensagem de conexão)
        if origin_id in clients:
            send_error(server_socket, address, "ID já em uso.")
        else:
            clients[origin_id] = address
            log(f"Cliente {origin_id} ({name.decode().strip()}) conectado.")
            server_socket.sendto(data, address)

    elif msg_type == 1:  # TCHAU (desconexão)
        if origin_id in clients:
            del clients[origin_id]
            log(f"Cliente {origin_id} desconectado.")
    
    elif msg_type == 2:  # MSG (mensagem normal)
        if origin_id not in clients:
            send_error(server_socket, address, "Cliente não registrado.")
        else:
            if dest_id == 0:
                # Broadcast para todos os clientes
                for client_address in clients.values():
                    server_socket.sendto(data, client_address)
            elif dest_id in clients:
                server_socket.sendto(data, clients[dest_id])
            else:
                send_error(server_socket, address, "Destinatário não encontrado.")
    
    elif msg_type == 3:  # ERRO
        log(f"Erro recebido de {origin_id}: {msg.decode().strip()}")

def send_error(server_socket, address, error_msg):
    error_msg = error_msg.encode().ljust(140, b'\x00')
    data = pack(MSG_FORMAT, 3, SERVER_ID, 0, len(error_msg), b'Server', error_msg)
    server_socket.sendto(data, address)
    log(f"Erro enviado para {address}: {error_msg.decode().strip()}")

def periodic_broadcast(server_socket):
    while True:
        time.sleep(60)
        message = f"Servidor ativo. Clientes conectados: {len(clients)}".encode().ljust(140, b'\x00')
        data = pack(MSG_FORMAT, 2, SERVER_ID, 0, len(message), b'Server', message)
        for client_address in clients.values():
            server_socket.sendto(data, client_address)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", 12345))  # Bind ao IP e porta
    log("Servidor iniciado na porta 12345.")
    
    # Iniciar thread de mensagens periódicas
    threading.Thread(target=periodic_broadcast, args=(server_socket,), daemon=True).start()
    
    while True:
        try:
            data, address = server_socket.recvfrom(1024)
            threading.Thread(target=handle_client, args=(data, address, server_socket)).start()
        except Exception as e:
            log(f"Erro ao receber dados: {e}")

if __name__ == "__main__":
    main()
