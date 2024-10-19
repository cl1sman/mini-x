import socket
import threading
from struct import pack, unpack
import time

MSG_FORMAT = "iiii20s140s"
#TIMEOUT = 5  # Timeout de 5 segundos para tentar reconectar
TIMEOUT = 20

def receive_messages(client_socket):
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            msg_type, origin_id, dest_id, msg_len, name, msg = unpack(MSG_FORMAT, data)
            
            if msg_type == 2:  # MSG
                print(f"Mensagem de {name.decode().strip()}: {msg.decode().strip()}")
            elif msg_type == 3:  # ERRO
                print(f"Erro recebido: {msg.decode().strip()}")
        except socket.timeout:
            print("Timeout: Nenhuma resposta do servidor. Tentando novamente...")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

def send_oi(client_socket, server_ip, server_port, client_id, client_name):
    oi_msg = pack(MSG_FORMAT, 0, client_id, 0, 0, client_name, b"")
    client_socket.sendto(oi_msg, (server_ip, server_port))
    print("Mensagem 'OI' enviada ao servidor.")

def send_tchau(client_socket, server_ip, server_port, client_id, client_name):
    tchau_msg = pack(MSG_FORMAT, 1, client_id, 0, 0, client_name, b"")
    client_socket.sendto(tchau_msg, (server_ip, server_port))
    print("Mensagem 'TCHAU' enviada ao servidor.")

def main():
    server_ip = input("Digite o IP do servidor: ")
    server_port = int(input("Digite a porta do servidor: "))
    client_id = int(input("Digite seu ID: "))
    client_name = input("Digite seu nome: ").encode().ljust(20, b'\x00')
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)  # Timeout para reconexão
    
    # Enviar mensagem OI para o servidor
    send_oi(client_socket, server_ip, server_port, client_id, client_name)
    
    # Iniciar thread para receber mensagens
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    
    try:
        while True:
            dest_id = int(input("Digite o ID do destinatário (0 para todos): "))
            message = input("Digite sua mensagem: ").encode().ljust(140, b'\x00')
            msg = pack(MSG_FORMAT, 2, client_id, dest_id, len(message), client_name, message)
            client_socket.sendto(msg, (server_ip, server_port))
    except KeyboardInterrupt:
        send_tchau(client_socket, server_ip, server_port, client_id, client_name)
        print("Encerrando conexão...")
        client_socket.close()

if __name__ == "__main__":
    main()
