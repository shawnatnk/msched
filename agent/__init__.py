import json
import datetime
import socket
import logging
import struct
from .command import Command

__version__ = '0.0.1'


class Agent:
    def __init__(self, master):
        self.master = master
        self.task = {}
        self.so = None

    def connect(self):
        self.so = socket.socket()
        self.so.connect(self.master)

    def encode(self, data):
        buf = json.dumps(data).encode()
        length = len(buf)
        return struct.pack('<l{}s'.format(length), length, buf)

    def heartbeat(self):
        """
        当前时间，版本，正在运行的任务
        :return: 
        """
        data = {
            'version'  : __version__,
            'timestamp': datetime.datetime.now().timestamp(),
            'task'     : self.task.get('current')
        }
        try:
            self.so.send(json.dumps(data).encode())
            if data.get('task') is None:
                buf = self.so.recv(4)
                length, _ = struct.unpack('<l', buf)
                buf = self.so.recv(length)
                data, _ = struct.unpack('<{}s'.format(length), buf)
                data = json.loads(data.decode())
                cmd = Command(data)
                cmd.run()

        except Exception as e:
            logging.error('send heartbeat err:{}'.format(e))
            self.connect()
