class XNode(object):
    guid_hash_handler = {}

    def __init__(self):
        pass

    @classmethod
    def register(cls, handler):
        raise NotImplementedError

    @classmethod
    def unregister(cls, handler):
        raise NotImplementedError


class NodeManager(XNode):
    @classmethod
    def register(cls, handler):
        if handler.node == -1:
            key = "{}-{}".format(handler.ip, handler.port)
            cls.guid_hash_handler[key] = handler
        else:
            pass

    @classmethod
    def unregister(cls, handler):
        key = "{}-{}".format(handler.ip, handler.port)
        if key in cls.guid_hash_handler:
            del cls.guid_hash_handler[key]


if __name__ == '__main__':
    nm = NodeManager()
