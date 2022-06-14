import json
import socket
import struct
import threading


from message import save_message
from message import get_messages


MAX_HEADER_SIZE = 2 ** 16 - 1
PREHEADER_SIZE = 2


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.conn = None
        # self.addr = None
        self.send_header = {
            'Content-type': 'application/json',
            'Content-encoding': 'utf-8'
        }
        self._read_buffer = b''
        self.response_type = ''
        self.name = ''
        self.threads = []

    def bind(self):
        self.sock.bind((self.host, self.port))

    def handle_client(self, conn):
        while True:
            self.recieve(conn)

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
        self.response(conn, body)
        return {
            'header': header,
            'body': body[0],
            'raw_body': body[1]
        }

    def response(self, conn, body):
        type = body[0]['action']
        # Will probably use a factory soon
        if type == 'login':
            response = {
                'action': 'login',
                'result': 'ok',
                'errors': []
            }
            self.name = body[0]['params']['name']
        elif type == 'send_messages':
            all_messages = body[0]['params']['messages']
            for i in all_messages:
                save_message(body[0]['params']['messages'][0]['to'], self.name, i['msg'])
            response = {
                'action': 'send_messages',
                'result': 'ok',
                'errors': []
            }
        elif type == 'logout':
            response = {
                'action': 'logout',
                'result': 'ok',
                'errors': []
            }
        elif type == 'get_messages':
            message = get_messages(self.name)
            response = {
                'action': 'get_messages',
                'result': 'ok',
                'messages': message,
                'errors': []
            }
            
        send_response = json.dumps(response)
        self.send(send_response, conn)

    def send(self, message, conn):
        body = bytes(message.encode('utf-8'))
        header = self._header(len(body))
        preheader = self._preheader(len(header))
        message = preheader + header + body
        # send the message
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

    # def log(self, username, type, error):
    #     format = (f'<{datetime.datetime.now()}> (ISO 8601):<{username}>:<{type}>:<{error}>')
    #     with open('log.txt', 'a') as f:
    #         f.write(format)

    # def close(self):
    #     self.conn.close()


chat_server = ChatServer('127.0.0.1', 65432)

chat_server.bind()
chat_server.listen()

# chat_server.accept()
# message = chat_server.recieve()
# print(message)
# while message:
#     message = chat_server.recieve()
#     print(message)
# chat_server.close()
