import unittest
from Server.requesthandler import GetRequest
from Server.requesthandler import SendRequest
from Server.requesthandler import LogoutRequest
from Server.requesthandler import LoginRequest



class TestGetRequest(unittest.TestCase):
    def setUp(self):
        self.get = GetRequest()

    def test_valid_response(self):
        body = {'action': 'get_messages', 'params': {'last_read': None}}
        username = 'test'
        assertion = {'body': {'action': 'get_messages',
                              'errors': [],
                              'messages': ['Hello'],
                              'result': ''},
                     'header': {'Content-encoding': 'utf-8',
                                'Content-length': 77,
                                'Content-type': 'application/json'},
                     'raw_body': '{"action": "get_messages", "result": "", "messages": '
                     '["Hello"], "errors": []}'}
        result = self.get.response(body, username)
        self.assertIsInstance(result, (str))
        self.assertEqual(result, assertion)


if __name__ == '__main__':
    unittest.main()
