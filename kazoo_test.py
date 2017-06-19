import logging
import threading
from kazoo.client import KazooClient, DataWatch
from gxx_func import *

logging.basicConfig(level=logging.INFO)
client = KazooClient(hosts='127.0.0.1:2181')
client.start()


client.create('/guoxx')
# client.create('/guoxx/t1', value=b"hello zk")
# client.ensure_path('/guoxx/1/2')
#
# data, stat = client.get('/guoxx/t1')
# p(data)
#
# ret = client.exists('/guoxx')
# p(ret)
#
# ret = client.get_children('/guoxx', )
# p(ret, "get_children")
#
# ret = client.set('/guoxx/1', b"111")
# p(ret,"set")
#
# client.ensure_path('/guoxx/1/2')
# ret = client.delete('/guoxx/1', recursive=True)
# p(ret)

# 事务

# watch

@client.DataWatch('/guoxx/1/2')
def watch(*args, **kwargs):
    p(args)
    p(kwargs)

# @client.ChildrenWatch


e = threading.Event()

try:
    e.wait()
except KeyboardInterrupt:
    e.set()
