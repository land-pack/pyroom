from __future__ import absolute_import

import logging
import ujson
from tornado import websocket
from pyroom.events.broker import BrokerServerDispatch
from pyroom.core.node import NodeManager

logger = logging.getLogger(__name__)

clients = []
broker_server_dispatch = BrokerServerDispatch()


class BrokerServerHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        clients.append(self)
        NodeManager.register(self)

    def on_message(self, message):
        """
        :param message: A dict type, as below example:
        {
            "method": "check_in",
            "body":{}
        }
        :return: write thing back
        """
        data = ujson.loads(message)
        method = data.get("method")
        body = data.get("body")
        getattr(broker_server_dispatch, method, getattr(broker_server_dispatch, "default"))(body)
        response = broker_server_dispatch.response
        self.write_message(response)

    def on_close(self):
        NodeManager.unregister(self)
        clients.remove(self)
