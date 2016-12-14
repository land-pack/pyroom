from __future__ import absolute_import

import logging
from tornado import websocket
from pyroom.events.broker import BrokerServerDispatch

logger = logging.getLogger(__name__)

clients = []


class BrokerServerHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        clients.append(self)

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        clients.remove(self)
