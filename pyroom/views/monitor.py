from __future__ import absolute_import

from collections import defaultdict

from tornado import web
from tornado import gen

from ..views import BaseHandler


class BrokerMonitor(BaseHandler):
    def get(self):
        self.write("Hello Node Information")