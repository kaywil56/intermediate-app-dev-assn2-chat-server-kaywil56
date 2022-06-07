import json
import socket
import struct

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
    
    def bind(self):
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen()
    
    def accept(self):
        self.conn, self.addr = self.sock.accept()
    
    def recieve(self):
        return self.conn.recv(1024)
    
    def close(self):
        self.conn.close()


chat_server = ChatServer('127.0.0.1', 65432)

chat_server.bind()
chat_server.listen()
chat_server.accept()
print(chat_server.recieve())
chat_server.close()
