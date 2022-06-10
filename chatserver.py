import json
import socket
import struct

MAX_HEADER_SIZE = 2 ** 16 - 1
PREHEADER_SIZE = 2


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
        self.send_header = {
            'Content-type': 'application/json',
            'Content-encoding': 'utf-8'
        }
        self._read_buffer = b''
        self.response_type = ''

    def bind(self):
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen()

    def accept(self):
        self.conn, self.addr = self.sock.accept()

    def recieve(self):
        header_len = self._read_preheader()
        header = self._read_header(header_len)
        body = self._read_body(header)
        type = body[0]['action']
        self._response(type)
        return {
            'header': header,
            'body': body[0],
            'raw_body': body[1]
        }

    def _response(self, type):
        response = {
            'action': type,
            'result': 'ok',
            'errors': []
        }

        send_response = json.dumps(response)

        body = bytes(send_response.encode('utf-8'))
        header = self._header(len(body))
        preheader = self._preheader(len(header))
        message = preheader + header + body
        self.conn.sendall(message)

    def _preheader(self, length):
        return struct.pack('>H', length)

    def _header(self, body_length):
        hdr = self.send_header
        hdr['Content-length'] = body_length
        hdr_str = json.dumps(hdr)
        return bytes(hdr_str.encode('utf-8'))

    def _read_body(self, header):
        body_len = header.get('Content-length')
        body_bytes = b''
        body_str = ''
        body = None
        body_bytes = self._read(body_len)
        body_str = body_bytes.decode('utf-8')
        body = json.loads(body_str)
        return body, body_str

    def _read_preheader(self):
        ph_bytes = self._read(PREHEADER_SIZE)
        return struct.unpack('>H', ph_bytes)[0]

    def _read_header(self, length):
        hdr_bytes = self._read(length)
        hdr_str = hdr_bytes.decode('utf-8')
        return json.loads(hdr_str)

    def _read(self, length):
        while len(self._read_buffer) < length:
            self._read_sock()
        result = self._read_buffer[:length]
        self._read_buffer = self._read_buffer[length:]
        return result

    def _read_sock(self):
        self._read_buffer += self.conn.recv(1024)

    def close(self):
        self.conn.close()


chat_server = ChatServer('127.0.0.1', 65432)

chat_server.bind()
chat_server.listen()
chat_server.accept()
print(chat_server.recieve())
print(chat_server.recieve())
chat_server.close()
