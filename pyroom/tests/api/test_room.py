from __future__ import absolute_import

import unittest
import requests
import time


class TestRoomByApi(unittest.TestCase):
    def setUp(self):
        self.uid = '123'
        self.r = requests.get('http://127.0.0.1:2332/api/join?uid=%s' % self.uid)

    def test_1_book(self):
        content = self.r.content
        self.assertEqual(content, 'ok')

    def test_2_check_in_by_http(self):
        r = requests.get('http://127.0.0.1:2332/api/checkin?uid=%s' % self.uid)
        content = r.content
        self.assertEqual(content, 'check_in_ok')
        time.sleep(6)
        r = requests.get('http://127.0.0.1:2332/api/checkin?uid=%s' % self.uid)
        content = r.content
        self.assertEqual(content, 'check_in_bad')


if __name__ == '__main__':
    unittest.main()
