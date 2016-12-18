from __future__ import absolute_import

import unittest
import time
from pyroom.core.room import RoomManager


class RoomTest(unittest.TestCase):
    def setUp(self):
        self.manager = RoomManager

    def test_1_book(self):
        room_name = self.manager.book('123')
        self.assertEqual(room_name, 'room_0')
        self.assertEqual(self.manager.uid_to_room, {'123': 'room_0'})
        self.manager.book('456')
        self.assertEqual(self.manager.uid_to_room, {'123': 'room_0', '456': 'room_0'})
        self.manager.book('789')
        self.assertEqual(self.manager.uid_to_room, {'123': 'room_0', '456': 'room_0', '789': 'room_0'})

    def test_2_cancel(self):
        self.manager.cancel('123')
        self.assertEqual(self.manager.uid_to_room, {'456': 'room_0', '789': 'room_0'})

    def test_3_book_again(self):
        self.manager.book('111')
        self.assertEqual(self.manager.uid_to_room, {'111': 'room_0', '456': 'room_0', '789': 'room_0'})

    def test_4_book_more(self):
        self.manager.book('112')
        self.manager.book('113')
        self.manager.book('114')
        self.manager.book('115')
        self.manager.book('116')
        self.manager.book('117')
        self.manager.book('118')
        self.assertEqual(self.manager.uid_to_room,
                         {'111': 'room_0', '456': 'room_0', '789': 'room_0', '112': 'room_1', '113': 'room_1',
                          '114': 'room_1', '115': 'room_2', '116': 'room_2', '117': 'room_2', '118': 'room_3'})

    def test_5_cancel_book(self):
        self.manager.cancel('111')
        self.assertEqual(self.manager.uid_to_room,
                         {'456': 'room_0', '789': 'room_0', '112': 'room_1', '113': 'room_1',
                          '114': 'room_1', '115': 'room_2', '116': 'room_2', '117': 'room_2', '118': 'room_3'})
        self.manager.book('222')
        self.assertEqual(self.manager.uid_to_room,
                         {'222': 'room_0', '456': 'room_0', '789': 'room_0', '112': 'room_1', '113': 'room_1',
                          '114': 'room_1', '115': 'room_2', '116': 'room_2', '117': 'room_2', '118': 'room_3'})

    def test_6_check_in(self):
        flag = self.manager.check_in('222')
        self.assertEqual(flag, True)
        flag = self.manager.check_in('222')
        self.assertEqual(flag, True)
    #     time.sleep(6)
    #     flag = self.manager.check_in('456')
    #     self.assertEqual(flag, False)


if __name__ == '__main__':
    unittest.main()
