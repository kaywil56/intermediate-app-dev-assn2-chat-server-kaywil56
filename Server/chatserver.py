import json
import socket
import struct
import threading
from requesthandler import request_factory
from user import User
from datetime import datetime

MAX_HEADER_SIZE = 2 ** 16 - 1
PREHEADER_SIZE = 2

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_header = {
            'Content-type': 'application/json',
            'Content-encoding': 'utf-8'
        }
        self._read_buffer = b''
        self.users = []
        self.user = User()

    def bind(self):
        self.sock.bind((self.host, self.port))

    def handle_client(self, conn):
        while True:
            print(self.recieve(conn))

    def listen(self):
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, ))
            thread.start()

    def recieve(self, conn):
        header_len = self._read_preheader(conn)
        header = self._read_header(header_len, conn)
        body = self._read_body(header, conn)
        type = body[0]['action']
        request = request_factory(type)
        response = request.response(body, self.user)
        errors = str(response['result'])
        self._log(type, errors)
        send_response = json.dumps(response)
        self.send(send_response, conn)
    
    def send(self, message, conn):
        body = bytes(message.encode('utf-8'))
        header = self._header(len(body))
        preheader = self._preheader(len(header))
        message = preheader + header + body
        conn.sendall(message)

    def _preheader(self, length):
        return struct.pack('>H', length)

    def _header(self, body_length):
        hdr = self.send_header
        hdr['Content-length'] = body_length
        hdr_str = json.dumps(hdr)
        return bytes(hdr_str.encode('utf-8'))

    def _read_body(self, header, conn):
        body_len = header.get('Content-length')
        body_bytes = b''
        body_str = ''
        body = None
        body_bytes = self._read(body_len, conn)
        body_str = body_bytes.decode('utf-8')
        body = json.loads(body_str)
        return body, body_str

    def _read_preheader(self, conn):
        ph_bytes = self._read(PREHEADER_SIZE, conn)
        return struct.unpack('>H', ph_bytes)[0]

    def _read_header(self, length, conn):
        hdr_bytes = self._read(length, conn)
        hdr_str = hdr_bytes.decode('utf-8')
        return json.loads(hdr_str)

    def _read(self, length, conn):
        while len(self._read_buffer) < length:
            self._read_sock(conn)
        result = self._read_buffer[:length]
        self._read_buffer = self._read_buffer[length:]
        return result

    def _read_sock(self, conn):
        self._read_buffer += conn.recv(1024)

    def _log(self, type, error):
        date_time = datetime.utcnow().isoformat()
        format = (f'{date_time} (ISO 8601):{self.user.username}:{type}:{error}')
        with open('log.txt', 'a') as f:
            f.write(format + '\n')

def main():
    chat_server = ChatServer('127.0.0.1', 65432)
    chat_server.bind()
    chat_server.listen()

if __name__ == '__main__':
    main()
