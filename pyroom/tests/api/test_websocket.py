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


if __name__ == '__main__':
    unittest.main()
