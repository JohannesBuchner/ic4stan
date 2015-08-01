"""
Just a front-end for the diagnostics of pymc

Author: Johannes Buchner (C) 2015
License: AFL (like pymc)
"""

import pymc
import numpy

from pymc.diagnostics import raftery_lewis, gelman_rubin, effective_n


def _effective_n(x, s2):
	m, n = x.shape
	negative_autocorr = False
	t = 1
	def variogram(t):
		return (sum(sum((x[j][i] - x[j][i-t])**2 for i in range(t,n)) 
			for j in range(m)) / (m*(n - t)))
	rho = numpy.ones(n)
	t2low = 0
	t2high = (n - 1) / 2
	t2mid = n / 2
	
	while True:
		print t
	

if __name__ == '__main__':
	import sys, os
	
	results = []
	filenames = sys.argv[1:]
	for filename in filenames:
		print 'Chain %s' % filename
		data = numpy.load(filename)
		nparams = 1
		uparams = []
		params_names = []
		for k, v in data.iteritems():
			if k == 'lp__': continue
			param_length = numpy.product(list(v.shape)[1:])
			nparams += param_length
			params_names += [k] * param_length
			uparams.append(v)
		params_flat = [numpy.concatenate([pi.flatten() for pi in row]) for row in zip(*uparams)]
		for name, x in zip(params_names, numpy.transpose(params_flat)):
			print '  parameter %s' % name
			nmin, kthin, nburn, nprec, kmind = raftery_lewis(x, q=0.1, r=0.01, verbose=False)
			print '    Raftery-Lewis (q=0.1, r=0.01): skip %d, use %d (of %d)' % (nburn, nprec, len(x))
			nmin, kthin, nburn, nprec, kmind = raftery_lewis(x, q=0.025, r=0.005, verbose=False)
			print '    Raftery-Lewis (q=0.025, r=0.005): skip %d, use %d (of %d)' % (nburn, nprec, len(x))
		results.append(params_flat)
	
	if len(filenames) > 1:
		print 'Chain group convergence'
		
		results = numpy.transpose(results)
		print results.shape
		for name, xx in zip(params_names, results):
			chains = numpy.transpose(xx)
			print '  parameter %s:' % name, chains.shape
			print '    Gelman-Rubin:', gelman_rubin(chains)
			#print '    Effective sample size:', effective_n(chains)
	else:
		print 'Chain group convergence not computed, pass more than one dataset'
		






