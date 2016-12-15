import time
from tornado import ioloop


class BaseRoomManager(object):
    uid_hash_ttl = {}
    uid_hash_ttl_flag = {}

    def __init__(self):
        pass

    @classmethod
    def book(cls, uid):
        """
        Check if there are some empty room available at first,
        if no open new room!
        :param uid:
        :return:
        """
        raise NotImplementedError

    @classmethod
    def cancel(cls, uid):
        """
        Call cancel if current node are unavailable!
        :param uid:
        :return:
        """
        raise NotImplementedError

    @classmethod
    def check_in(cls, uid):
        """
        Confirm user has checking, agree only if the user has not expire!
        and then delete element from uid_hash_ttl_flag!
        :param uid:
        :return:
        """
        raise NotImplementedError

    @classmethod
    def check_out(cls, uid):
        """
        if user has no operate anything kick it off, or maybe they leave self!
        :param uid:
        :return:
        """
        raise NotImplementedError

    @classmethod
    def is_expire(cls, uid, max_time=5):
        """
        If user haven't check in during a given time, will release this room!
        :param uid:
        :param max_time:
        :return:
        """
        latest = cls.uid_hash_ttl.get(uid, None)
        if not latest:
            return True
        if time.time() - latest > max_time:
            return True
        else:
            return False

    @classmethod
    def set_ttl(cls, uid):
        """
        if user book room success, will clock the timer and set flag!
        :param uid:
        :return:
        """
        cls.uid_hash_ttl[uid] = time.time()
        cls.uid_hash_ttl_flag[uid] = True

    @classmethod
    def update_ttl_flag(cls, uid):
        """
        Check if the current uid whether expire! if expire set flag to False
        :param uid:
        :return:
        """
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
        cls.set_ttl(uid)
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
