from threading import Event
import socket
import json
import struct
import os
import datetime
import logging

__version__ = '0.0.1'


def encode(json_data):
    data = json.dumps(json_data).encode()
    return struct.pack('<l{}s'.format(len(data)), len(data), data)


def decode(bytes_data):
    return json.loads(bytes_data.decode())


class Agent:
    def __init__(self, master, frequency=10):
        self.event = Event()
        self.master = master
        self.frequency = frequency
        self.so = None
        self.id = os.uname().nodename
        self.tasks = {}

    def connect(self):
        try:
            self.so = socket.socket()
            self.so.connect(self.master)
        except ConnectionRefusedError as e:
            logging.log(logging.ERROR, e)

    def heartbeat_packet(self):
        data = {
            'id': self.id,
            'version': __version__,
            'timestamp': datetime.datetime.now().timestamp()
        }
        return encode(data)

    def heartbeat(self):
        packet = self.heartbeat_packet()
        try:
            self.so.send(packet)
            if self.tasks.get('current') is None:
                print('In None')
                buf = self.so.recv(4)
                length, *_ = struct.unpack('<l', buf)
                buf = self.so.recv(length)
                task = decode(buf)
                logging.log(logging.ERROR, task)
        except Exception as e:
            self.connect()

    def start(self):
        while not self.event.is_set():
            self.heartbeat()
            self.event.wait(self.frequency)

    def shutdown(self):
        self.event.set()
