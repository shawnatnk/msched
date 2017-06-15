from subprocess import Popen, PIPE, STDOUT
from concurrent.futures import ThreadPoolExecutor


class Command:
    def __init__(self, task):
        self.task = task
        self.executor = ThreadPoolExecutor(max_workers=1)

    def __run(self):
        with Popen(['/bin/bash', '-l', '-c', self.script],
                   stdout=PIPE,
                   stderr=STDOUT,
                   start_new_session=True) as proc:
            code = proc.wait(self.timeout)
            out, _ = proc.communicate()
            self.task['code'] = code
            self.task['output'] = out

    def run(self):
        self.executor.submit(self.__run)
