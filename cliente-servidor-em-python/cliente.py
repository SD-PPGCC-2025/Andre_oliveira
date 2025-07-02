import threading
import socket
import time
import random

HOST = '127.0.0.1'
PORT = 65432

def cliente(id):
    """Simula um cliente que solicita serviços e espera se necessário"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Cliente {id} conectado à oficina.")

        while True:
            print(f"Cliente {id} está escolhendo acessórios...")
            time.sleep(random.uniform(1, 3))  # Simula tempo escolhendo acessórios

            # Solicita um terminal ao servidor
            print(f"Cliente {id} solicitando um terminal para serviço...")
            s.sendall("SOLICITAR_TERMINAL".encode())

            resposta = s.recv(1024).decode()
            if resposta.startswith("TERMINAL_CONCEDIDO"):
                servico = resposta.split(":")[1]
                print(f"Cliente {id} está fazendo {servico} (usando um terminal)...")
                time.sleep(random.uniform(2, 5))  # Simula tempo do serviço

                # Libera o terminal
                print(f"Cliente {id} liberando terminal...")
                s.sendall("LIBERAR_TERMINAL".encode())
                s.recv(1024)  # Confirmação do servidor

            else:
                print(f"Cliente {id} aguardando terminal disponível...")

            time.sleep(random.uniform(1, 3))  # Aguarda antes de tentar novamente

# Criando e rodando múltiplos clientes
for i in range(5):
    time.sleep(1)  # Para evitar que todos os clientes se conectem ao mesmo tempo
    threading.Thread(target=cliente, args=(i,)).start()