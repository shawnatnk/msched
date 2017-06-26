from subprocess import Popen, PIPE, STDOUT
from gxx_funcs import p, d

script = 'ip a'

with Popen(['/bin/bash', '-l', '-c', script], stderr=STDOUT, stdout=PIPE) as proc:
    proc.wait()
    out = proc.communicate()
    p(out)
