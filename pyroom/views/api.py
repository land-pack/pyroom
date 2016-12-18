from __future__ import absolute_import

from ..views import BaseHandler
from pyroom.core.room import RoomManager


class JoinHandler(BaseHandler):
    def get(self):
        uid = self.get_argument("uid")
        ret = RoomManager.book(uid)
        if ret:
            self.write('ok')
        else:
            self.write("bad")


class CheckInHandler(BaseHandler):
    def get(self):
        uid = self.get_argument("uid")
        ret = RoomManager.check_in(uid)
        if ret:
            self.write('check_in_ok')
        else:
            self.write("check_in_bad")
