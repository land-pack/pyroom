from __future__ import absolute_import

import unittest
import requests
import time
import ujson


class TestRoomByApi(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_book(self):
        uid = '111'
        r = requests.get('http://127.0.0.1:2332/api/join?uid=%s' % uid)
        response = ujson.loads(r.content)
        self.assertEqual(response, {'status': '100', 'room': 'room_0'})

    def test_2_check_in_by_http(self):
        uid = '111'
        r = requests.get('http://127.0.0.1:2332/api/checkin?uid=%s' % uid)
        content = r.content
        self.assertEqual(content, 'check_in_ok')
        time.sleep(6)
        r = requests.get('http://127.0.0.1:2332/api/checkin?uid=%s' % uid)
        content = r.content
        self.assertEqual(content, 'check_in_bad')

    def test_3_book_more(self):
        uid = '222'
        r = requests.get('http://127.0.0.1:2332/api/join?uid=%s' % uid)
        uid = '333'
        r = requests.get('http://127.0.0.1:2332/api/join?uid=%s' % uid)
        uid = '444'
        r = requests.get('http://127.0.0.1:2332/api/join?uid=%s' % uid)
        response = ujson.loads(r.content)
        self.assertEqual(response, {'status': '100', 'room': 'room_1'})

    def test_4_check_in_after_is_expire(self):
        uid = '222'
        r = requests.get('http://127.0.0.1:2332/api/checkin?uid=%s' % uid)
        content = r.content
        self.assertEqual(content, 'check_in_ok')
        time.sleep(6)
        uid = '333'
        r = requests.get('http://127.0.0.1:2332/api/checkin?uid=%s' % uid)
        content = r.content
        self.assertEqual(content, 'check_in_bad')

    def test_5_book_if_have_old_room(self):
        uid = '555'
        r = requests.get('http://127.0.0.1:2332/api/join?uid=%s' % uid)
        response = ujson.loads(r.content)
        self.assertEqual(response, {'status': '100', 'room': 'room_0'})


if __name__ == '__main__':
    unittest.main()
