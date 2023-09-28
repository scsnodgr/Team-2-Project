import socket
import time

# server's IP address and port number
HOST = socket.gethostbyname(socket.gethostname())
HOST_PORT = 7501

# all clients IP addresses and port numbers
CLIENTS = socket.gethostbyname(socket.gethostname())
CLIENT_PORTS = 7500

# specifies socket type (internet and UDP)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# binds socket to the server's IP address and port number
server.bind((HOST, HOST_PORT))

# game start countdown timer
time.sleep(3)

# server sends variable amount of bytes to all clients
message = '202'
server.sendto(message.encode('utf-8'), (CLIENTS, CLIENT_PORTS))
print("Sending code to client: " + message)

timer = 0
while True:
    # server receives 1024 bytes of information from client
    received_information, address = server.recvfrom(1024)
    print("Information recieved from client: " + received_information.decode('utf-8'))

    # server sends variable amount of bytes to all clients
    message = '1'
    server.sendto(message.encode('utf-8'), (CLIENTS, CLIENT_PORTS))

    # sleep to simulate end code being sent at the end of the game
    timer = timer + 1
    if timer == 4:
        break

# server sends variable amount of bytes to all clients
message = '221'
server.sendto(message.encode('utf-8'), (CLIENTS, CLIENT_PORTS))
print("Sending code to client: " + message)