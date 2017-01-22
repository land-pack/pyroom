import uuid
import ujson


class NodeInformation(object):

    def __init__(self, handler, rooms=0):
        self.ip = handler.ip
        self.port = handler.port
        self.node_id = "{}-{}".format(self.ip, self.port)
        self.rooms = rooms
        self.room_set = set()
        self.origin_node_id = handler.node
        setattr(handler, 'node', self.node_id)
        setattr(handler, 'ni', self)

class NodeManager(dict):
    nodeid_hash_nodeinfo = {}
    max_rooms = 50

    def register(self, handler): 
        node_info = NodeInformation(handler)
        self.__setitem__(node_info.node_id, node_info)
        if node_info.origin_node_id == "-1":      
            return ujson.dumps({'method': 'connect', 'node': node_info.node_id})
        else:
            return ujson.dumps({'method': 'recovery'})

    def unregister(self, handler):
        release_rooms = handler.ni.room_set
        self.__delitem__(handler.ni.node_id)
        return release_rooms

    def gen_room_name(self):
        for node_id, node_info in self.iteritems():
            if node_info.rooms < self.max_rooms:
                node_info.rooms += 1
                room_name = '{}-{}'.format(node_info.node_id,uuid.uuid1())
                node_info.room_set.add(room_name)
                return room_name
        return None


class Handler(object):
    pass


if __name__ == '__main__':
    handler = Handler()
    setattr(handler, 'ip', '127.0.0.1')
    setattr(handler, 'port', '1999')
    setattr(handler, 'node', '-1')

    handler2 = Handler()
    setattr(handler2, 'ip', '127.0.0.2')
    setattr(handler2, 'port', '1992')
    setattr(handler2, 'node', '-1')
    manager = NodeManager()
    assert manager.register(handler) == ujson.dumps({"node":"127.0.0.1-1999","method":"connect"})
    assert manager.register(handler) == ujson.dumps({"method":"recovery"})
    manager.register(handler2)
    print manager.gen_room_name()
    print manager.gen_room_name()
    print manager.gen_room_name()
    print manager.gen_room_name()
    print manager.gen_room_name()
    print manager.unregister(handler)
    print manager.unregister(handler2)