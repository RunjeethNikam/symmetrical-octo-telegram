"""
Helper module for the plot scripts.
"""

import re
import itertools
import matplotlib as m
import os

if os.uname()[0] == "Darwin":
    m.use("MacOSX")
else:
    m.use("Agg")
import matplotlib.pyplot as plt
import argparse
import math


# import termcolor as T

def read_list(fname, delim=','):
    lines = open(fname).readlines()
    ret = []
    for l in lines:
        ls = l.strip().split(delim)
        ls = list(map(lambda e: '0' if e.strip() == '' or e.strip() == 'ms' or e.strip() == 's' else e, ls))
        ret.append(ls)
    return ret


def col(n, obj=None, clean=lambda e: e):
    """A versatile column extractor.

    col(n, [1,2,3]) => returns the nth value in the list
    col(n, [ [...], [...], ... ] => returns the nth column in this matrix
    col('blah', { ... }) => returns the blah-th value in the dict
    col(n) => partial function, useful in maps
    """
    if obj == None:
        def f(item):
            return clean(item[n])

        return f
    if type(obj) == type([]):
        if len(obj) > 0 and (type(obj[0]) == type([]) or type(obj[0]) == type({})):
            return map(col(n, clean=clean), obj)
    if type(obj) == type([]) or type(obj) == type({}):
        try:
            return clean(obj[n])
        except:
            # print T.colored('col(...): column "%s" not found!' % (n), 'red')
            return None
    # We wouldn't know what to do here, so just return None
    # print T.colored('col(...): column "%s" not found!' % (n), 'red')
    return None