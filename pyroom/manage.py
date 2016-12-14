from pyroom.app import PyRoom
from options import options
from pyroom.urls import settings
from pyroom.urls import handlers

if __name__ == '__main__':
    pyroom = PyRoom(options=options, handlers=handlers, **settings)
    pyroom.start()
