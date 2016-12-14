from pyroom.core.room import RoomManager


class DispatchResponse(object):
    def write(self, status, body):
        response = {"status": status, "body": body}
        self.response = response


class BrokerServerDispatch(DispatchResponse):
    def check_out(self, body):
        uid = body.get("uid")
        RoomManager.check_out(uid)
        self.write(100, {})

    def check_in(self, body):
        uid = body.get("uid")
        RoomManager.check_in(uid)

    def ping(self, body):
        pass

    def default(self, body):
        pass
