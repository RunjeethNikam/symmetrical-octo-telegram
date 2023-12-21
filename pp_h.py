import argparse
import matplotlib as mpl
import os as os_utils

mac = "MacOSX"
agg = "Agg"

if os_utils.uname()[0] == "Darwin":
    mpl.use(mac)
else:
    mpl.use(agg)

import matplotlib.pyplot as plt
import argparse


def read_file_lines(file_path, delimiter=","):
    lines = open(file_path).readlines()
    result = []
    for line in lines:
        elements = line.strip().split(delimiter)
        elements = list(
            map(
                lambda e: "0"
                if e.strip() == "" or e.strip() == "ms" or e.strip() == "s"
                else e,
                elements,
            )
        )
        result.append(elements)
    return result


def extract_column(index, data=None, lmd=lambda e: e):
    """A versatile column extractor.

    extract_column(index, [1,2,3]) => returns the nth value in the list
    extract_column(index, [ [...], [...], ... ] => returns the nth column in this matrix
    extract_column('blah', { ... }) => returns the blah-th value in the dict
    extract_column(index) => partial function, useful in maps
    """
    if data is None:
        return lambda iem: lmd(iem[index])
    if isinstance(data, list):
        if len(data) > 0 and (
            isinstance(data[0], list) or isinstance(data[0], dict)
        ):
            return map(extract_column(index, lmd=lmd), data)
    if isinstance(data, list) or isinstance(data, dict):
        try:
            return lmd(data[index])
        except:
            return None
    return None


# The rest of the code remains unchanged




def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--files",
        "-f",
        help="Ping output files to plot",
        required=True,
        action="store",
        nargs="+",
    )

    parser.add_argument(
        "--xlimit",
        help="Upper limit of x axis, data after ignored",
        type=float,
        default=8
    )

    parser.add_argument(
        "--out",
        "-o",
        help="Output png file for the plot.",
        default=None
    )

    args = parser.parse_args()
    return args
