import tornado
from tornado.httpclient import HTTPRequest
from tornado.web import Application
from tornado.websocket import websocket_connect
from tornado.testing import AsyncHTTPTestCase, gen_test


def message_processed_callback(*args, **kwargs):
    print 'Callback(args=%r, kwargs=%r)' % (args, kwargs)


class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def initialize(self):
        self.io_loop = tornado.ioloop.IOLoop.instance()

    def on_message(self, message):
        future = self.on_some_message(message)
        print 'The future:', future
        self.io_loop.add_future(future, message_processed_callback)

    @tornado.gen.coroutine
    def on_some_message(self, message):
        print 'Before sleep'
        yield tornado.gen.sleep(3)
        print 'After sleep'
        self.write_message(message)


class ChatTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return Application([
            ('/rt', RealtimeHandler),
        ])

    @gen_test
    def test_reply(self):
        request = HTTPRequest('ws://127.0.0.1:%d/rt' % self.get_http_port())
        ws = yield websocket_connect(request)

        ws.write_message('Hi')

        response = yield ws.read_message()
        print 'Response:', response