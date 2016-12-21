import ujson
from pyroom.core.room import RoomManager


class DispatchResponse(object):
    def write(self, status, mid, body):
        """
        :param status: request status code (100 ok)
        :param mid: request message id
        :param body: request body
        :return: write to `response` property!
        """
        response = {"status": str(status), "mid": str(mid), "body": body}
        self.response = ujson.dumps(response)


class BrokerServerDispatch(DispatchResponse):
    def check_in(self, body):
        uid = body.get("uid")
        if RoomManager.check_in(uid):
            self.write(100, 1000, {'info': 'check in success'})
        else:
            RoomManager.check_in(uid)
            self.write(100, 1001, {'info': 'check in failure'})

    def check_out(self, body):
        uid = body.get("uid")
        if RoomManager.check_out(uid):
            self.write(100, 1002, {})
        else:
            self.write(100, 1003, {})

    def ping(self, body):
        pass

    def default(self, body):
        pass
