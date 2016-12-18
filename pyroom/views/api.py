from __future__ import absolute_import

import ujson
from ..views import BaseHandler
from pyroom.core.room import RoomManager
from pyroom.core.node import NodeManager


class JoinHandler(BaseHandler):
    def get(self):
        """
        status:
        100 --> ok
        101 --> no room name available
        102 --> no node for use
        :return:
        """
        uid = self.get_argument("uid")
        room_name = RoomManager.book(uid)
        if room_name:
            try:
                node_info = NodeManager.landing(room_name)
                response = {'room': room_name, 'status': '100', 'node': node_info.node, 'ip': node_info.ip,
                            'port': node_info.port}
            except ValueError:
                RoomManager.cancel(uid=uid)
                response = {'room': room_name, 'status': '102'}
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
