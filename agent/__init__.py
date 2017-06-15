import json
import datetime
import socket
import logging
import struct
import threading
from .command import Command

__version__ = '0.0.1'


class Agent:
    def __init__(self, master):
        self.master = master
        self.tasks = {} # GIL 内置数据结构，线程安全？？
        self.so = None
        self.event = threading.Event()

    def connect(self):
        self.so = socket.socket()
        self.so.connect(self.master)

    def encode(self, data):
        buf = json.dumps(data).encode()
        length = len(buf)
        return struct.pack('<l{}s'.format(length), length, buf)

    def heartbeat(self):
        data = {
            'version'  : __version__,
            'timestamp': datetime.datetime.now().timestamp(),
            'task'     : self.tasks.get('current')
        }
        try:
            self.so.send(json.dumps(data).encode())
            if data.get('task') is None:
                buf = self.so.recv(4)
                length, _ = struct.unpack('<l', buf)
                buf = self.so.recv(length)
                data, _ = struct.unpack('<{}s'.format(length), buf)
                task = json.loads(data.decode())
                cmd = Command(task)
                future = cmd.run()
                if future is not None:
                    future.add_done_callback(lambda: self.tasks.pop('current', None))
                self.tasks['current'] = task

        except Exception as e:
            logging.error('send heartbeat err:{}'.format(e))
            self.connect()

    def start(self):
        while not self.event.is_set():
            self.heartbeat()
            self.event.wait(1)

    def shutdown(self):
        self.event.set()
