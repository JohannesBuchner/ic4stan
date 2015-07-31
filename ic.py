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

def dic(log_like):
	D = -2 * log_like
	Dmean = D.mean()
	#pD_spiegelhalter = Dmean - D(theta_mean)
	pD_gelman = 0.5 * numpy.var(D)
	DIC = pD_gelman + Dmean
	return DIC

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
	return -2 * log_like.max() + k * log(n)

if __name__ == '__main__':
	import sys
	results = {}
	filenames = sys.argv[1:]
	for filename in filenames:
		data = numpy.load(filename)
		l = data['lp__']
		nparams = 1
		for k in data.keys():
			if k == 'lp__': continue
			nparams += numpy.product(list(data[k].shape)[1:])
		print '%d parameters' % nparams
		nsamples = len(l)
		result = waic(l)
		result['dic'] = dic(l)
		result['aic'] = aic(l, nparams)
		result['maxlike'] = maxlike(l)
		for k, v in result.iteritems():
			results[k] = results.get(k, []) + [v]
			print '%-20s | %-10s | %.1f' % (filename, k, v)
		print
	print '%-10s : mean\tstd' % 'criterion'
	for k, v in results.iteritems():
		print '%-10s : %.1f\t%.1f' % (k, numpy.mean(v), numpy.std(v))
	

