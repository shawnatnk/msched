from subprocess import Popen, PIPE, STDOUT


class Command(object):
    def __init__(self, script):
        self.script = script

    def run(self):
        with Popen(['/bin/bash', '-l', '-c', self.script], stderr=STDOUT, stdout=PIPE) as p:
            p.wait()
            out, _ = p.communicate()
            return out
