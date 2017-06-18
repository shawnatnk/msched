import socket
from threading import Event
import datetime
import json
import struct

__version__ = '0.0.1'


class Agent(object):
    event = Event()

    def __init__(self, master):
        self.master = master
        self.so = None
        self.task = {}

    def connect(self):
        so = socket.socket()
        so.connect(self.master)
        self.so = so

    def encode(self, data):
        length = len(data)
        return struct.pack('<4l{}s'.format(length), data)

    def heartbeat(self):
        data = {
            "version"  : __version__,
            "timestamp": datetime.datetime.now().timestamp(),
            "task"     : self.tasks.get('current', None)
        }

        data = json.dumps(data).encode()
        data = self.encode(data)
        self.so.send(data)

        if not self.task.get('current'):
            self.so.recv()



    def start(self):
        while not self.event.is_set():
            self.heartbeat()
            self.event.wait(1)

    def shutdown(self):
        self.event.set()
