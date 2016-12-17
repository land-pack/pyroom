from __future__ import absolute_import

import unittest
from pyroom.core.room import RoomManager


class RoomTest(unittest.TestCase):
    def setUp(self):
        self.manager = RoomManager

    def test_book(self):
        room_name = self.manager.book('123')
        self.assertEqual(room_name, 'room_0')
        self.assertEqual(self.manager.uid_to_room, {'123': 'room_0'})
        room_name = self.manager.book('456')
        self.assertEqual(self.manager.uid_to_room, {'123': 'room_0', '456': 'room_0'})

    def test_cancel(self):
        self.manager.cancel('123')
        self.assertEqual(self.manager.uid_to_room, {'456': 'room_0'})


if __name__ == '__main__':
    unittest.main()
