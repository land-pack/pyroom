import ujson
from pyroom.core.room import RoomManager


class DispatchResponse(object):
    def write(self, status, mid, body):
        response = {"status": str(status), "mid": str(mid), "body": body}
        self.response = ujson.dumps(response)


class BrokerServerDispatch(DispatchResponse):
    def check_in(self, body):
        uid = body.get("uid")
        if RoomManager.is_expire(uid):
            self.write(100, 1001, {})
        else:
            RoomManager.check_in(uid)
            self.write(100, 1000, {})

    def check_out(self, body):
        uid = body.get("uid")
        RoomManager.check_out(uid)
        self.write(100, 1002, {})

    def ping(self, body):
        pass

    def default(self, body):
        pass
