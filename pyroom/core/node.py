class NodeInformation(object):
    """
    All property will be domain load to this object!
    @property ip ('127.0.0.1')
    @property port (9001)
    @property node (2)
    @property handler (websocket handler instance)
    @property mac ('127.0.0.1-9001'
    Usage:
        ni = NodeInformation()
        ni.ip = '127.0.0.1'
        ni.port = 9001
        ni.node = 2
        ni.handler = handler
    """

    def __init__(self, ip, port, node, handler, mac, rooms=0):
        self.ip = ip
        self.port = port
        self.node = node
        self.handler = handler
        self.mac = mac
        self.rooms = rooms
        self.room_set = set()


class XNode(object):
    guid_hash_handler = {}
    room_to_node = {}
    node_map = {}
    node_index = 0
    max_rooms = 12

    def __init__(self):
        pass

    @classmethod
    def register(cls, handler):
        raise NotImplementedError

    @classmethod
    def unregister(cls, handler):
        raise NotImplementedError

    @classmethod
    def get_node(cls, prefix='node_'):
        node_name = prefix + str(cls.node_index)
        cls.node_index += 1
        return node_name

    @classmethod
    def landing(cls, room):
        """
        Checking, if room already install on someone node, just return that node!
        else checking, the lack level hash, get node which almost fill full one!
        :param room:
        :return:
        """
        raise NotImplementedError


class NodeManager(XNode):
    @classmethod
    def register(cls, handler):
        if int(handler.node) == -1:
            mac = "{}-{}".format(handler.ip, handler.port)
            node = cls.get_node()
            ni = NodeInformation(ip=handler.ip, port=handler.port, node=node, handler=handler, mac=mac)
            cls.guid_hash_handler[mac] = ni
            cls.node_map[node] = ni
            return ni
        else:
            # TODO recovery mode
            pass

    @classmethod
    def unregister(cls, handler):
        mac = "{}-{}".format(handler.ip, handler.port)
        if mac in cls.guid_hash_handler:
            ni = cls.guid_hash_handler[mac]
            del cls.guid_hash_handler[mac]
            node = ni.node
            del cls.node_map[node]

    @classmethod
    def landing(cls, room):
        for node in cls.node_map:
            if cls.node_map[node].rooms < cls.max_rooms:
                if room in cls.node_map[node].room_set:
                    return cls.node_map[node]
                else:
                    cls.node_map[node].room_set.add(room)
                    cls.node_map[node].rooms += 1
                    return cls.node_map[node]
        raise ValueError("No more node available!")


if __name__ == '__main__':
    nm = NodeManager()
