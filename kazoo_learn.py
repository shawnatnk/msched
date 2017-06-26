from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch
from gxx_func import *
from threading import Event

zk = KazooClient(['192.168.13.10:2181'])
zk.start()

# 删除节点<recursive=True>递归删除
zk.delete('/t', recursive=True)

# 创建节点
zk.create('/t')
zk.ensure_path('/t/0/0')
zk.ensure_path('/t/0/1')

# 设置数据
# set (1)path必须存在(2)value必须是bytes
zk.set('/t', b'hello zoo')

# 获取数据
data, stat = zk.get('/t')

# 获取子节点, 返回值为list
children = zk.get_children('/t/0')  # --> ['0','1']

# 判断是否存在, 返回节点状态或None
stat = zk.exists('/t/0/q')


# Watchers
def watch(*args, **kwargs):
    p(args)
    p(kwargs)


children = zk.get_children('/t/0', watch=watch)

# Transactions


# Lock

zk.stop()
zk.close()

event = Event()
while True:
    try:
        event.wait()
    except KeyboardInterrupt:
        event.set()
