import socket
import random
import time

# server's IP address and port number
HOST = socket.gethostbyname(socket.gethostname())
HOST_PORT = 7501

# client's IP address and port number
CLIENT = socket.gethostbyname(socket.gethostname())
CLIENT_PORT = 7500

# specifies socket type (internet and UDP)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# binds socket to the clients's IP address and port number
client.bind((CLIENT, CLIENT_PORT))

# while start code 202 not received
received_information = ''
while received_information != '202':
    # client receives 1024 bytes of information from server
    received_information, address = client.recvfrom(1024)
    print("Information recieved from server: " + received_information.decode('utf-8'))

# equipment ids of players
red1 = input('Enter equipment id of red player 1 ==> ')
red2 = input('Enter equipment id of red player 2 ==> ')
green1 = input('Enter equipment id of green player 1 ==> ')
green2 = input('Enter equipment id of green player 2 ==> ')

# while end code 221 not received
while received_information != '221':
    # random assignment of red player
    if random.randint(1, 2) == 1:
        redplayer = red1
    else:
        redplayer = red2

    # random assignment of green player
    if random.randint(1, 2) == 1:
        greenplayer = green1
    else:
        greenplayer = green2

    # random assignment of message layout
    if random.randint(1, 2) == 1:
        message = str(redplayer) + ":" + str(greenplayer)
    else:
        message = str(greenplayer) + ":" + str(redplayer)

    # client sends variable amount of bytes to server
    client.sendto(message.encode('utf-8'), (HOST, HOST_PORT))
    print("Sending equipment code to server: " + message)

    # client receives 1024 bytes of information from server
    received_information, address = client.recvfrom(1024)
    print("Information recieved from server: " + received_information.decode('utf-8'))

    # sleep to simulate players slowly joining
    time.sleep(random.randint(1, 3))