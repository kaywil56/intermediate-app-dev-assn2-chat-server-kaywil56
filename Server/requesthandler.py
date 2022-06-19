""" A factory pattern for sending back the right response. """

from message import save_message
from message import get_messages


class GetRequest:
    """ A class for handling a get request"""

    def response(self, body, user):
        """ Calls the get_messages method to retreive a clients messages and returns the appropriate responsec"""
        response = {
            'action': 'get_messages',
            'result': '',
            'messages': [],
            'errors': []
        }
        if user.is_logged_in:
            user.last_read = body[0]['params']['last_read']
            try:
                messages = get_messages(user.username, user.last_read)
                response['messages'] = messages
            except Exception as e:
                response['result'] = 'error'
                response['errors'].append(str(e))
            return response
        else:
            response['result'] = 'error'
            response['errors'].append('User must be logged in.')
            return response


class SendRequest:
    """ A class for handling a send request"""

    def response(self, body, user):
        """Calls the send_messages method to save a clients messages and returns the appropriate response"""
        response = {
            'action': 'send_messages',
            'result': 'ok',
            'errors': []
        }
        if user.is_logged_in:
            try:
                all_messages = body[0]['params']['messages']
                for i in all_messages:
                    to = body[0]['params']['messages'][0]['to']
                    msg = i['msg']
                    save_message(to, user.username, msg)
            except Exception as e:
                response['result'] = 'error'
                response['errors'].append(str(e))
            return response
        else:
            response['result'] = 'error'
            response['errors'].append('User must be logged in.')
            return response


class LogoutRequest:
    """ A class for handling a logout request"""

    def response(self, body, user):
        """ Sets the current user logged in and returns the appropriate response """
        response = {
            'action': 'logout',
            'result': 'ok',
            'errors': []
        }
        if user.is_logged_in:
            user.is_logged_in = False
            return response
        else:
            response['result'] = 'error'
            response['errors'].append('User must be logged in.')
            return response


class LoginRequest:
    """ A class for handling a login request"""

    def response(self, body, user):
        """ Sets the current user logged out and returns the appropriate response """
        user.is_logged_in = True
        user.username = body[0]['params']['name']
        response = {
            'action': 'login',
            'result': 'ok',
            'errors': []
        }
        return response


def request_factory(type):
    """ Selects the right response based on the given request type"""
    REQUEST_TYPES = {
        'get_messages': GetRequest,
        'send_messages': SendRequest,
        'logout': LogoutRequest,
        'login': LoginRequest
    }

    return REQUEST_TYPES[type]()
