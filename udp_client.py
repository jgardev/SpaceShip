
import socket

PORT = 5553
BUFFER_SIZE = 10


def format_data(channel, data):
    return str.encode(channel+':'+data+'\n')

def decode_data(data:str):
    return data[:1].split(":")

class UDPClient:

    def __init__(self, host):
        self.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server = (host, PORT)
        self.active = False

    def send(self, channel, data):
        self.socket.sendto(format_data(channel,data), self.server)

    def recieve(self):
        while self.active:
            data = self.socket.recvfrom(BUFFER_SIZE)
            self.on_recieve(str(data[0]), data[1])

    def on_recieve(self, data, addr):
        pass


class UDPServer:

    def __init__(self):
        self.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.active = False

        self.socket.bind((socket.gethostname(), PORT))

    def send(self, addr, channel, data):
        self.socket.sendto(format_data(channel, data), addr)

    def recieve(self):
        while self.active:
            data = self.socket.recvfrom(BUFFER_SIZE)
            self.on_recieve(data[0],data[1])
        
    def on_recieve(self, data, addr):
        pass        
