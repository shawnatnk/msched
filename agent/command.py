from subprocess import Popen, PIPE, STDOUT
from concurrent.futures import ThreadPoolExecutor
from threading import Event
import os


class Command:
    executor = ThreadPoolExecutor(max_workers=1)
    event = Event()

    def __init__(self, task):
        self.task = task
        self.executor = ThreadPoolExecutor(max_workers=1)

    def __run(self):
        self.event.set()
        with Popen(['/bin/bash', '-l', '-c', self.script],
                   stdout=PIPE,
                   stderr=STDOUT,
                   start_new_session=True) as proc:
            code = proc.wait(self.timeout)
            out, _ = proc.communicate()
            self.task['code'] = code
            self.task['output'] = out
        self.event.clear()

    def run(self):
        if not self.event.is_set():
            self.executor.submit(self.__run)
