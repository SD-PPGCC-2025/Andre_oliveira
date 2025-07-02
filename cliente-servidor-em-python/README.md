# cliente-servidor-em-python
# Um clássico problema em sistemas distribuídos -  problema dos Filósofos comerciantes. 
import socket
import threading
import random
import time

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 65432
NUM_TERMINAIS = 2  # Número de terminais disponíveis
terminais_disponiveis = NUM_TERMINAIS
lock = threading.Lock()

def handle_cliente(conn, addr):
    """Gerencia as requisições do cliente"""
    global terminais_disponiveis
    print(f"[NOVO CLIENTE] Conectado: {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data == "SOLICITAR_TERMINAL":
                with lock:  # Evita condições de corrida
                    if terminais_disponiveis > 0:
                        terminais_disponiveis -= 1
                        servico = random.choice(["Revisão", "Troca de óleo", "Pintura", "Balanceamento", "Troca de pneus"])
                        conn.sendall(f"TERMINAL_CONCEDIDO:{servico}".encode())
                    else:
                        conn.sendall("TERMINAL_OCUPADO".encode())

            elif data == "LIBERAR_TERMINAL":
                with lock:
                    terminais_disponiveis += 1
                conn.sendall("TERMINAL_LIBERADO".encode())

        except ConnectionResetError:
            break  # Cliente desconectou

    print(f"[DESCONECTADO] Cliente {addr} saiu.")
    conn.close()

def servidor():
    """Inicia o servidor"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVIDOR] Oficina rodando em {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_cliente, args=(conn, addr))
            thread.start()

servidor()
