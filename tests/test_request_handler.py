import unittest
from Server.requesthandler import *
from unittest.mock import Mock, patch


class TestGetRequest(unittest.TestCase):
    def setUp(self):
        self.get = GetRequest()

    def test_valid_response(self):
        body = {'action': 'get_messages', 'params': {'last_read': None}}
        user = Mock()
        user.username = 'test'
        assertion = {
                        'action': 'get_messages',
                        'errors': ['You have no messages.'],
                        'messages': [],
                        'result': 'error',           
                    }
        result = self.get.response(body, user)
        self.assertEqual(result, assertion)


class TestSendRequest(unittest.TestCase):
    def setUp(self):
        self.send = SendRequest()

    def test_valid_response(self):
        body =  {'action': 'send_messages', 'params': {'messages': [{'to': 'greg', 'msg': 'Hey, greg'}]}}
        user = Mock()
        user.username = 'test'
        assertion = {
                        'action': 'send_messages',
                        'errors': [],
                        'result': 'ok',           
                    }
        result = self.send.response(body, user)
        self.assertEqual(result, assertion)


class TestLoginRequest(unittest.TestCase):
    def setUp(self):
        self.login = LoginRequest()

    def test_valid_response(self):
        body = {'action': 'login', 'params': {'name': 'k'}}
        user = Mock()
        user.username = 'test'
        assertion = {
                        'action': 'login',
                        'errors': [],
                        'result': 'ok'
                    }
        result = self.login.response(body, user)
        self.assertEqual(result, assertion)


class TestLogoutRequest(unittest.TestCase):
    def setUp(self):
        self.logout = LogoutRequest()

    def test_valid_response(self):
        body = {'action': 'logout', 'params': None}
        user = Mock()
        user.username = 'test'
        assertion = {
                        'action': 'logout',
                        'errors': [],
                        'result': 'ok'
                    }
        result = self.logout.response(body, user)
        self.assertEqual(result, assertion)


if __name__ == '__main__':
    unittest.main()
