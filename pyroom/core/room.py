import time
from tornado import ioloop


class BaseRoomManager(object):
    uid_hash_ttl = {}
    uid_hash_ttl_flag = {}

    def __init__(self):
        pass

    @classmethod
    def book(cls, uid):
        raise NotImplementedError

    @classmethod
    def cancel(cls, uid):
        raise NotImplementedError

    @classmethod
    def check_in(cls, uid):
        raise NotImplementedError

    @classmethod
    def check_out(cls, uid):
        raise NotImplementedError

    @classmethod
    def is_expire(cls, uid, max_time=5):
        latest = cls.uid_hash_ttl.get(uid, None)
        if not latest:
            return True
        if latest > max_time:
            return True
        else:
            return False

    @classmethod
    def set_ttl(cls, uid):
        cls.uid_hash_ttl[uid] = time.time()
        cls.uid_hash_ttl_flag[uid] = True

    @classmethod
    def update_ttl_flag(cls, uid):
        if cls.is_expire(uid):
            cls.uid_hash_ttl_flag[uid] = False
            return True
        return False

    @classmethod
    def loop_check_ttl(cls):
        """
        Loop by tornado, check each user expire!
        Usage:
        checker = RoomManager.loop_check_ttl
        ioloop.PeriodicCallback(checker, 1000).start()
        :return:
        """
        changed_list = []
        for uid in cls.uid_hash_ttl:
            changed = cls.update_ttl_flag(uid)
            if changed:
                changed_list.append(uid)

        for uid in changed_list:
            del cls.uid_hash_ttl[uid]


class RoomManager(BaseRoomManager):
    @classmethod
    def book(cls, uid):
        print 'book a room for', uid

    @classmethod
    def cancel(cls, uid):
        pass

    @classmethod
    def check_in(cls, uid):
        if cls.update_ttl_flag(uid):
            # TODO verify ok
            pass
        else:
            # forbidden
            pass

    @classmethod
    def check_out(cls, uid):
        pass


if __name__ == '__main__':
    RoomManager.book('123')
    RoomManager.set_ttl('123')
    RoomManager.loop_check_ttl()
    print RoomManager.uid_hash_ttl_flag
    # time.sleep(5)
    # print RoomManager.uid_hash_ttl_flag
