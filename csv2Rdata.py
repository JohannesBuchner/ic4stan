"""
Converts csv files written by Stan (http://mc-stan.org) into Rdata files
that Stan can read for initialisation.
Use if you want to start a Stan run from the final point of another Stan run.

Author: Johannes Buchner (c) 2015
License: GPLv3
"""

import numpy
import sys

print 'loading data ...'
f = open(sys.argv[1])
lines = [l for l in f.readlines() if not l.startswith('#')]
header = lines[0].split(',')

variables_dimensions = dict()
variables_setters = []
variables = {}
variable_names = []

for var in header:
	if '.' not in var:
		variable_names.append(var)
		variables_dimensions[var] = tuple()
		variables_setters.append(dict(var=var))
	else:
		parts = var.split('.')
		trunk = parts[0]
		variable_names.append(trunk)
		pos = [int(p) for p in parts[1:]]
		dim = list(pos)
		if trunk in variables_dimensions:
			dim_prev = variables_dimensions[trunk]
			for i in range(len(pos)):
				dim[i] = max(dim[i], dim_prev[i])
		
		variables_dimensions[trunk] = tuple(dim)
		variables_setters.append(dict(var=trunk, pos=pos))

print 'creating variables...'
for var, dim in variables_dimensions.iteritems():
	print var, dim
	variables[var] = numpy.zeros(dim)

print 'setting variables...'

for l in lines[1:]:
	for i, value_str in enumerate(l.split(',')):
		value = float(value_str)
		var = variables_setters[i]['var']
		pos1 = variables_setters[i].get('pos', None)
		if pos1 is None:
			variables[var] = value
		else:
			pos0 = tuple([d - 1 for d in pos1]) # 0-indexed for numpy
			variables[var][pos0] = value
	break # only use the first data line

for var in sorted(variables.keys()):
	value = variables[var]
	if len(numpy.shape(value)) == 0:
		if int(value) == value:
			value = int(value)
	else:
		if numpy.all(value.astype(int) == value):
			variables[var] = value.astype(int)
	print var, variables[var]

print 'storing as Rdump ...'
import pystan
if 'lp__' in variables:
	del variables['lp__']
outfilename = sys.argv[1].rstrip('.csv') + '.Rdata'
pystan.misc.stan_rdump(variables, outfilename)


