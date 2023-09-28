import socket

class UDP:
    # initialize socket
    def __init__(self):
        # server's IP address and port number
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.HOST_PORT = 7501

        # all clients IP addresses and port numbers
        self.CLIENTS = socket.gethostbyname(socket.gethostname())
        self.CLIENT_PORTS = 7500

        # specifies socket type (internet and UDP)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # binds socket to the server's IP address and port number
        self.server.bind((self.HOST, self.HOST_PORT))

    # server receives 1024 bytes of information from client
    def receive_data(self):
        received_information, address = self.server.recvfrom(1024)
        print("Information recieved from client: " + received_information.decode('utf-8'))
        return received_information.decode('utf-8')
        
    # server sends variable amount of bytes to all clients
    def broadcast_data(self, message):
        self.server.sendto(message.encode('utf-8'), (self.CLIENTS, self.CLIENT_PORTS))
        print("Sending code to client: " + message)