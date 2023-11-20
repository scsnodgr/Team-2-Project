import socket
import random

HOST = socket.gethostbyname(socket.gethostname())
BROADCAST_PORT = 7501

print('This program will generate some test traffic for 2 players on the red ')
print('team as well as 2 players on the green team')
print('')

red1 = input('Enter equipment id of red player 1 ==> ')
red2 = input('Enter equipment id of red player 2 ==> ')
green1 = input('Enter equipment id of green player 1 ==> ')
green2 = input('Enter equipment id of green player 2 ==> ')

# Create datagram sockets
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# wait for start from game software
print ('')
print ('Waiting for start from game_software\n')

# flag to exchange addresses with server
UDPClientSocket.sendto(("1111:1111").encode('utf-8'), (HOST, BROADCAST_PORT))

received_data = ' '
while received_data != '202':
	received_data, address = UDPClientSocket.recvfrom(1024)
	received_data = received_data.decode('utf-8')
	print ('Received ' + received_data + ' from ' + str(address))
print ('')

# create events, random player and order
while True:
	if random.randint(1,2) == 1:
		redplayer = red1
	else:
		redplayer = red2

	if random.randint(1,2) == 1:
		greenplayer = green1
	else: 
		greenplayer = green2	

	if random.randint(1,2) == 1:
		message = str(redplayer) + ":" + str(greenplayer)
	else:
		message = str(greenplayer) + ":" + str(redplayer)

	print("Sending " + message + " to " + str((HOST, BROADCAST_PORT)))
	UDPClientSocket.sendto(str.encode(str(message)), (HOST, BROADCAST_PORT))

	# receive answer from game softare
	received_data, address = UDPClientSocket.recvfrom(1024)
	received_data = received_data.decode('utf-8')
	print ('Received ' + received_data + ' from ' + str(address))
	print ('')
	if received_data == '221':
		break
	
print("Program complete")