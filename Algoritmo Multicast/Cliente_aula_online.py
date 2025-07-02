import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

# Cria o socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Permite múltiplos clientes na mesma máquina
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # escuta em todas as interfaces

# Junta-se ao grupo multicast
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Aguardando aula ao vivo...")
while True:
    data, addr = sock.recvfrom(1024)
    print(f"[{addr[0]}] {data.decode()}")
