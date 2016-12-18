import time
import requests


class BaseRoomManager(object):
    uid_hash_ttl = {}
    uid_hash_ttl_flag = {}
    room_to_uid_set = {}
    uid_to_room = {}
    room_lack_level = {}
    room_size = 3
    lack_level_set = {key: set() for key in range(1, room_size + 1)}
    room_name_index = 0

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
        latest = cls.uid_hash_ttl.get(uid)
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

    # @classmethod
    # def update_ttl_flag(cls, uid):
    #     """
    #     Check if the current uid whether expire! if expire set flag to False
    #     :param uid:
    #     :return:
    #     """
    #     if cls.is_expire(uid):
    #         cls.uid_hash_ttl_flag[uid] = False
    #         return True
    #     return False

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
            r = requests.get('http://127.0.0.1:5000?uid=%s' % uid)
            is_expired = cls.is_expire(uid=uid)
            if is_expired:
                changed_list.append(uid)
                cls.cancel(uid=uid)

        for uid in changed_list:
            del cls.uid_hash_ttl[uid]


class RoomManager(BaseRoomManager):
    @classmethod
    def gen_room_name(cls, prefix='room_'):
        room_name = prefix + str(cls.room_name_index)
        cls.room_name_index += 1
        return room_name

    @classmethod
    def new_room(cls, uid):
        size = cls.room_size
        room_name = cls.gen_room_name()
        cls.room_to_uid_set[room_name] = set()
        cls.room_to_uid_set[room_name].add(uid)
        cls.room_lack_level[room_name] = size - 1
        cls.lack_level_set[size - 1].add(room_name)
        return room_name

    @classmethod
    def old_room(cls, uid):
        size = cls.room_size
        for r in range(1, size + 1):
            set_length = len(cls.lack_level_set[r])
            if set_length > 0:
                room_name = cls.lack_level_set[r].pop()
                lack_level = cls.room_lack_level[room_name]
                if lack_level == 1:
                    del cls.room_lack_level[room_name]
                else:
                    cls.room_lack_level[room_name] = lack_level - 1
                    cls.lack_level_set[r - 1].add(room_name)
                cls.room_to_uid_set[room_name].add(uid)
                return room_name
        raise ValueError("No old room available!")

    @classmethod
    def book(cls, uid):
        try:
            room_name = cls.old_room(uid)
        except ValueError:
            room_name = cls.new_room(uid)
        cls.set_ttl(uid)
        cls.uid_to_room[uid] = room_name
        return room_name

    @classmethod
    def cancel(cls, uid):
        room_name = cls.uid_to_room[uid]
        lack_level = cls.room_lack_level.get(room_name, None)
        if lack_level is not None:
            cls.lack_level_set[lack_level].remove(room_name)
            cls.lack_level_set[lack_level + 1].add(room_name)
            cls.room_lack_level[room_name] = lack_level + 1
        else:
            cls.lack_level_set[1].add(room_name)
            cls.room_lack_level[room_name] = 1
        cls.room_to_uid_set[room_name].remove(uid)
        del cls.uid_to_room[uid]
        return cls

    @classmethod
    def check_in(cls, uid):
        if cls.uid_hash_ttl.get(uid, None):
            # agree check in
            del cls.uid_hash_ttl[uid]
            return True
        else:
            # forbidden check in
            return False

    @classmethod
    def check_out(cls, uid):
        cls.cancel(uid=uid)
