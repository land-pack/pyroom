from __future__ import absolute_import

from collections import defaultdict

from tornado import web
from tornado import gen

from ..views import BaseHandler
from pyroom.core.room import RoomManager


class BrokerMonitor(BaseHandler):
    def get(self):
        print 'room uid_hash_flag', RoomManager.uid_hash_ttl_flag
        self.write("Hello Node Information")
