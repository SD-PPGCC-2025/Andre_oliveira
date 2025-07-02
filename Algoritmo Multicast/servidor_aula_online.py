import socket
import time

MCAST_GRP = '224.1.1.1'  # Endereço do grupo multicast
MCAST_PORT = 5007        # Porta usada

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# TTL = 1 significa que o pacote não atravessa roteadores
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

print("Transmitindo aula ao vivo...")
mensagens = [
    "Bem-vindos à aula ao vivo!",
    "Hoje vamos falar sobre redes multicast.",
    "Multicast é eficiente para transmitir a mesma mensagem para vários destinos.",
    "Dúvidas? Mandem no chat!",
    "Até a próxima aula!"]

for msg in mensagens:
    sock.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
    print(f"Enviado: {msg}")
    time.sleep(2)  # intervalo entre mensagens
