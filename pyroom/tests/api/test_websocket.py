from __future__ import absolute_import

import unittest
import requests
import time
import ujson


class TestWebsocket(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_book(self):
        r = requests.get('http://127.0.0.1:2332/api/join?uid=111')
        self.assertEqual(200, r.status_code)
        content = r.content

        assume_response = {'room': 'room_0', 'status': '100', 'node': 'node_0', 'ip': '192.168.0.101',
                           'port': '9001'}
        self.assertEqual(ujson.loads(content), assume_response)


if __name__ == '__main__':
    unittest.main()
