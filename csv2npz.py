"""
Converts csv files written by Stan (http://mc-stan.org) into Rdata files
that Stan can read for initialisation.
Use if you want to start a Stan run from the final point of another Stan run.

Author: Johannes Buchner (c) 2015
License: GPLv3
"""

from __future__ import print_function
import numpy
import sys
from stancsvreader import readcsv

print('loading data ...')
variables = readcsv(sys.argv[1])

print('storing as npz ...')
outfilename = sys.argv[1].rstrip('.csv') + '.npz'
numpy.savez(outfilename, **variables)


