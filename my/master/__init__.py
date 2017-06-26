import socketserver
import json
import struct
import logging


def encode(json_data):
    data = json.dumps(json_data).encode()
    return struct.pack('<l{}s'.format(len(data)), len(data), data)


def decode(bytes_data):
    return json.loads(bytes_data.decode())


class MasterHandler(socketserver.BaseRequestHandler):
    def handle(self):
        length, *_ = self.request.recv(4)
        buf = self.request.recv(length)
        heartbeat, *_ = struct.unpack('<{}s'.format(length), buf)
        print(decode(heartbeat))
        self.request.send(encode({'a': 1}))


class Master:
    def __init__(self, address):
        self.address = address
        self.server = socketserver.ThreadingTCPServer(self.address, MasterHandler)

    def start(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
