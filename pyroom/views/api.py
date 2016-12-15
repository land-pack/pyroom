from __future__ import absolute_import

from ..views import BaseHandler
from pyroom.core.room import RoomManager


class JoinHandler(BaseHandler):
    def get(self):
        uid = self.get_argument("uid")
        print 'uid is', uid
        RoomManager.book(uid)
        self.write('welcome to join us')
