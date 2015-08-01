"""
Compute various information criteria from MCMC chains,
If multiple chains are provided, compute the deviation.

Author: Johannes Buchner (C) 2015
License: GPLv3

A useful resource is http://arxiv.org/abs/1307.5928
"""

import numpy
import scipy.misc

def waic(log_like):
	lpd = scipy.misc.logsumexp(log_like)
	p_waic = numpy.var(log_like)
	elpd_waic = lpd - p_waic
	waic = -2 * elpd_waic
	return dict(elpd_waic=elpd_waic, p_waic=p_waic, waic=waic)

def maxlike(log_like):
	return log_like.max()

def like_at_mean(log_like, uparams):
	# the mean is at 0, by definition of the normalised uparams
	#    and the standard deviation is 1.
	#    compute diagonal Mahalanobis distance to pick the closest point
	distances = []
	for row in zip(*uparams):
		# flatten parameters
		row_params_flat = numpy.concatenate([pi.flatten() for pi in row])
		# compute distance to 0
		distances.append(numpy.linalg.norm(row_params_flat))
	
	# pick the one with the smallest distance
	i = numpy.argmin(distances)
	#print 'mean parameters at %d of %d' % (i, len(distances))
	#print 'maximum likelihood at %d' % numpy.argmax(log_like)
	
	return log_like[i]

def dic(log_like, uparams):
	D = -2 * log_like
	Dmean = D.mean()
	Dat_param_mean = -2 * like_at_mean(log_like, uparams)
	pD_spiegelhalter = Dmean - Dat_param_mean
	DIC = pD_spiegelhalter + Dmean
	pD_gelman = 0.5 * numpy.var(D)
	DIC2 = pD_gelman + Dmean
	return dict(dic=DIC, dic_gelman=DIC2)


def dic(log_like, uparams):
	D = -2 * log_like
	log_like_mean = log_like.mean()
	Lat_param_mean = like_at_mean(log_like, uparams)
	pDIC = 2 * (Lat_param_mean - log_like_mean)
	pDICalt = 2 * numpy.var(log_like)
	DIC = -2 * Lat_param_mean + 2 * pDIC
	DICalt = -2 * Lat_param_mean + 2 * pDICalt
	return dict(dic=DIC, dic_gelman=pDICalt)

def aic(log_like, nparams):
	k = nparams
	return 2 * k - 2 * log_like.max()

def aicc(log_like, nparams, ndata):
	k = nparams
	n = ndata
	return aic(log_like, nparams) + 2 * k * (k + 1) / (n - k - 1)

def bic(log_like, nparams, ndata):
	k = nparams
	n = ndata
	return -2 * log_like.max() + k * numpy.log(n)

if __name__ == '__main__':
	import sys, os
	
	ndata = float(os.environ.get('NDATA', 'nan'))
	results = {}
	filenames = sys.argv[1:]
	for filename in filenames:
		data = numpy.load(filename)
		l = data['lp__']
		nparams = 1
		uparams = []
		for k, v in data.iteritems():
			if k == 'lp__': continue
			nparams += numpy.product(list(v.shape)[1:])
			uparams.append((v - v.mean(axis=0)) / v.std(axis=0))
		
		print '%d parameters' % nparams
		nsamples = len(l)
		result = waic(l)
		result.update(dic(l, uparams))
		result['aic'] = aic(l, nparams)
		result['maxlike'] = maxlike(l)
		if numpy.isfinite(ndata):
			result['aicc'] = aicc(l, nparams, ndata)
			result['bic'] = bic(l, nparams, ndata)
		for k, v in result.iteritems():
			results[k] = results.get(k, []) + [v]
			print '%-20s | %-10s | %.1f' % (filename, k, v)
		print
	print '%-10s : mean\tstd' % 'criterion'
	for k, v in results.iteritems():
		print '%-10s : %.1f\t%.1f' % (k, numpy.mean(v), numpy.std(v))
	

