from __future__ import absolute_import

import logging
import ujson
from tornado import websocket
from pyroom.events.broker import BrokerServerDispatch
from pyroom.core.node import NodeManager

logger = logging.getLogger(__name__)
broker_server_dispatch = BrokerServerDispatch()


class BrokerServerHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        """
        ws://127.0.0.1:2332/api/ws?port=9001&node=-1
        """
        logger.debug("New node register:\t\tip=%s\tport=%s", ip, port)
        setattr(self, 'host', self.request.remote_ip)
        setattr(self, 'port', self.get_argument("port"))
        setattr(self, 'node', self.get_argument("node"))
        try:
            response = NodeManager.register(self)
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise
        else:
            self.write_message(response)

    def on_message(self, message):
        """
        :param message: A dict type, as below example:
        {
            "method": "check_in",
            "body":{}
        }
        :return: write thing back
        """
        try:
            data = ujson.loads(message)
            method = data.get("method")
            body = data.get("body")
            getattr(broker_server_dispatch, method, getattr(broker_server_dispatch, "default"))(body)
            response = broker_server_dispatch.response
        except TypeError:
            response = 'p'
        self.write_message(response)

    def on_close(self):
        NodeManager.unregister(self)
