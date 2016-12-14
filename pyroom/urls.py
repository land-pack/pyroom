from __future__ import absolute_import

import os

from tornado.web import StaticFileHandler

from pyroom.views import websocket
from pyroom.views import monitor
from pyroom.views.error import NotFoundErrorHandler

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static")
)

handlers = [
    # Events WebSocket API
    (r"/api/ws", websocket.BrokerServerHandler),

    # Monitors
    (r"/monitor/broker", monitor.BrokerMonitor),
    # Static
    (r"/static/(.*)", StaticFileHandler),

    # Error
    (r".*", NotFoundErrorHandler)
]
