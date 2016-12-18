from __future__ import absolute_import

import ujson
from ..views import BaseHandler
from pyroom.core.room import RoomManager


class JoinHandler(BaseHandler):
    def get(self):
        uid = self.get_argument("uid")
        room_name = RoomManager.book(uid)
        if room_name:
            response = {'room': room_name, 'status': '100'}
            self.write(ujson.dumps(response))
        else:
            response = {'status': '101'}
            self.write(ujson.dumps(response))


class CheckInHandler(BaseHandler):
    def get(self):
        uid = self.get_argument("uid")
        ret = RoomManager.check_in(uid)
        if ret:
            self.write('check_in_ok')
        else:
            self.write("check_in_bad")
