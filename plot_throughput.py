import argparse
import matplotlib.pyplot as plt
import matplotlib as m
from matplotlib.ticker import LinearLocator
from pylab import figure
from helper import read_list, col

def parse_arguments():
    parser = argparse.ArgumentParser(description='Plot queue occupancy over time')
    parser.add_argument('--files', '-f', help='Throughput timeseries output to one plot',
                        required=True, action='store', nargs='+', dest='files')
    parser.add_argument('--legend', '-l', help='Legend to use if there are multiple plots. File names used as default.',
                        action='store', nargs='+', default=None, dest='legend')
    parser.add_argument('--out', '-o', help='Output png file for the plot.', default=None, dest='out')
    parser.add_argument('--labels', help='Labels for x-axis if summarizing; defaults to file names',
                        required=False, default=[], nargs='+', dest='labels')
    parser.add_argument('--xlimit', help='Upper limit of x axis, data after ignored', type=float, default=50)
    parser.add_argument('--every', help='If the plot has a lot of data points, plot one of every EVERY (x, y) point (default 1).',
                        default=1, type=int)

    return parser.parse_args()

def get_style(i):
    colors = ['red', 'blue', 'green', 'black']
    return {'color': colors[i % len(colors)]}

def plot_data(ax, files, legend, xlimit):
    for i, f in enumerate(sorted(files)):
        data = read_list(f)
        xaxis = map(float, col(0, data))
        throughput = map(float, col(1, data))
        throughput = [t for j, t in enumerate(throughput) if xaxis[j] <= xlimit]
        xaxis = [x for x in xaxis if x <= xlimit]

        ax.plot(xaxis, throughput, label=legend[i], lw=2, **get_style(i))
        ax.xaxis.set_major_locator(LinearLocator(6))

    if legend is not None:
        plt.legend()

def main():
    args = parse_arguments()

    m.rc('figure', figsize=(32, 12))
    fig = figure()
    ax = fig.add_subplot(111)

    plot_data(ax, args.files, args.legend, args.xlimit)

    plt.ylabel("Throughput (Mbits)")
    plt.grid(True)
    plt.xlabel("Seconds")
    plt.tight_layout()

    if args.out:
        print('saving to', args.out)
        plt.savefig(args.out)
    else:
        plt.show()

if __name__ == '__main__':
    main(
