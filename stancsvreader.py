"""
Converts csv files written by Stan (http://mc-stan.org) into a dictionary of 
numpy arrays.

Author: Johannes Buchner (c) 2015
License: GPLv3
"""
from __future__ import print_function
import numpy
import sys

def readcsv(filename):
	f = open(filename)
	lines = [l for l in f.readlines() if not l.startswith('#')]
	header = lines[0].split(',')

	variables_dimensions = dict()
	variables_setters = []
	variables = {}
	variables_all = {}
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

	print('creating variables...')
	for var in variables_dimensions.keys():
		dim = variables_dimensions[var]
		print('  ', var, dim)
		variables[var] = numpy.zeros(dim)

	print('setting variables...')

	for l in lines[1:]:
		if l.strip() == '': continue
		for i, value_str in enumerate(l.split(',')):
			value = float(value_str)
			var = variables_setters[i]['var']
			pos1 = variables_setters[i].get('pos', None)
			if pos1 is None:
				variables[var] = value
			else:
				pos0 = tuple([d - 1 for d in pos1]) # 0-indexed for numpy
				variables[var][pos0] = value
		for var in sorted(variables.keys()):
			value = variables[var]
			if len(numpy.shape(value)) == 0:
				if int(value) == value:
					value = int(value)
			else:
				if numpy.all(value.astype(int) == value):
					variables[var] = value.astype(int)
			#print var, variables[var]
			variables_all[var] = variables_all.get(var, []) + [variables[var]]
	
	for var in sorted(variables.keys()):
		variables[var] = numpy.array(variables_all[var])
		#print var, variables[var].shape
	return variables

