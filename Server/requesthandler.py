from message import save_message
from message import get_messages


class GetRequest:
    def response(self, body, user):
        user.last_read = body[0]['params']['last_read']
        messages = get_messages(user.username, user.last_read)
        response = {
            'action': 'get_messages',
            'result': 'ok',
            'messages': messages,
            'errors': []
        }
        return response


class SendRequest:
    def response(self, body, user):
        all_messages = body[0]['params']['messages']
        for i in all_messages:
            to = body[0]['params']['messages'][0]['to']
            msg = i['msg']
            save_message(to, user.username, msg)
        response = {
            'action': 'send_messages',
            'result': 'ok',
            'errors': []
        }
        return response


class LogoutRequest:
    def response(self, body, user):
        response = {
            'action': 'logout',
            'result': 'ok',
            'errors': []
        }
        return response


class LoginRequest:
    def response(self, body, user):
        user.username = body[0]['params']['name']
        response = {
            'action': 'login',
            'result': 'ok',
            'errors': []
        }
        return response


def request_factory(type):
    REQUEST_TYPES = {
        'get_messages': GetRequest,
        'send_messages': SendRequest,
        'logout': LogoutRequest,
        'login': LoginRequest  
    }

    return REQUEST_TYPES[type]()