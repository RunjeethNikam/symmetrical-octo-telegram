import argparse
import matplotlib.pyplot as plt
import matplotlib as m
from matplotlib.ticker import LinearLocator
from pylab import figure
from helper import read_list, col

def parse_arguments():
    parser = argparse.ArgumentParser(description='Plot ping RTTs over time')
    parser.add_argument('--files', '-f', help='Ping output files to plot',
                        required=True, action='store', nargs='+')
    parser.add_argument('--xlimit', help='Upper limit of x axis, data after ignored',
                        type=float, default=8)
    parser.add_argument('--out', '-o', help='Output png file for the plot.', default=None)

    return parser.parse_args()

def plot_ping_rtts(ax, files, xlimit):
    for i, f in enumerate(files):
        data = read_list(f)
        xaxis = list(map(float, col(0, data)))
        rtts = list(map(float, col(1, data)))
        xaxis = [x - xaxis[0] for x in xaxis]
        rtts = [r * 1000 for j, r in enumerate(rtts) if xaxis[j] <= xlimit]
        xaxis = [x for x in xaxis if x <= xlimit]
        
        if "bbr" in files[i]:
            name = "bbr"
        else:
            name = "cubic"
        
        ax.plot(xaxis, rtts, lw=2, label=name)
        plt.legend()
        ax.xaxis.set_major_locator(LinearLocator(5))

def main():
    args = parse_arguments()

    m.rc('figure', figsize=(32, 12))
    fig = figure()
    ax = fig.add_subplot(111)

    plot_ping_rtts(ax, args.files, args.xlimit)

    plt.ylabel("RTT (ms)")
    plt.xlabel("Seconds")
    plt.grid(True)
    plt.tight_layout()

    if args.out:
        print('saving to', args.out)
        plt.savefig(args.out)
    else:
        plt.show()

if __name__ == '__main__':
    main()
