class BaseRoomManager(object):
    def __init__(self):
        pass

    @classmethod
    def book(cls, uid):
        raise NotImplementedError

    @classmethod
    def check_in(cls, uid):
        raise NotImplementedError

    @classmethod
    def check_out(cls, uid):
        raise NotImplementedError

    @classmethod
    def is_timeout(cls, uid):
        raise NotImplementedError


class RoomManager(BaseRoomManager):
    @classmethod
    def book(cls, uid):
        print 'book a room for', uid

    @classmethod
    def check_in(cls, uid):
        pass

    @classmethod
    def check_out(cls, uid):
        pass

    @classmethod
    def is_timeout(cls, uid):
        pass
