from subprocess import *
from multiprocessing import Process

default_dir = "."


def capture_packets(options="", fname="%s/capture.dmp" % default_dir, runner=None):
    cmd = "tcpdump -Z root -w {} {}; chmod +xwr {}".format(fname, options, fname)
    print(cmd)
    runner = Popen if runner is None else runner
    return runner(cmd, shell=True).wait()


def start_capture(outfile="capture.dmp"):
    monitor = Process(target=capture_packets, args=("", outfile))
    monitor.start()
    return monitor


def filter_capture(filt, infile="capture.dmp", outfile="filtered.dmp"):
    monitor = Process(
        target=capture_packets, args=("-r ./{} {}".format(infile, filt), outfile)
    )
    monitor.start()
    return monitor
