from subprocess import *

default_dir = '.'


def capture_packets(options="", fname='%s/capture.dmp' % default_dir, runner=None):
    cmd = "tcpdump -Z root -w {} {}; chmod +xwr {}".format(fname, options, fname)
    print(cmd)
    runner = Popen if runner is None else runner
    return runner(cmd, shell=True).wait()
