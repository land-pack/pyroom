class XNode(object):
    guid_hash_handler = {}

    def __init__(self):
        pass

    def register(self, handler):
        raise NotImplementedError

    def unregister(self, handler):
        raise NotImplementedError


class NodeManager(XNode):
    def register(self, handler):
        if handler.node == -1:
            key = "{}-{}".format(handler.ip, handler.port)
            self.guid_hash_handler[key] = handler
        else:
            pass

    def unregister(self, handler):
        key = "{}-{}".format(handler.ip, handler.port)
        del self.guid_hash_handler[key]


if __name__ == '__main__':
    nm = NodeManager()
