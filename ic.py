import numpy
import scipy.misc

"""
WAIC <- function(x)
{
lppd <- sum (log(rowMeans(exp(x))))
pWAIC1 <- 2*sum(log(rowMeans(exp(x))) - rowMeans(x))
pWAIC2 <- sum(.rowVars(x))
WAIC <- -2*lppd + 2*pWAIC2
return(list(WAIC=WAIC, lppd=lppd, pWAIC=pWAIC2, pWAIC1=pWAIC1))
}
"""

#WAIC = T + V / nsamples
#WBIC = -Ew()

"""
totals <- function(pointwise) {
	N <- length(pointwise[[1L]])
	total <- unlist_lapply(pointwise, sum)
	se <- sqrt(N * unlist_lapply(pointwise, var))
	as.list(c(total, se))
}
"""

def total(v):
	N = len(v)
	return v.sum(), N**0.5 * v.std()

"""
#' @importFrom matrixStats colVars
pointwise_waic <- function(log_lik) {
	lpd <- logColMeansExp(log_lik)
	p_waic <- colVars(log_lik)
	elpd_waic <- lpd - p_waic
	waic <- -2 * elpd_waic
	nlist(elpd_waic, p_waic, waic)
}
"""

def logColMeansExp(x):
	S = len(x)
	return colLogSumExps(x) - log(S)

def pointwise_waic(log_lik):
	lpd = scipy.misc.logsumexp(log_lik, axis=1)
	p_waic = numpy.var(log_lik, axis=1)
	elpd_waic = lpd - p_waic
	waic = -2 * elpd_waic
	aic = log_lik.max(axis=1)
	return dict(elpd_waic=elpd_waic, p_waic=p_waic, waic=waic)

"""
waic <- function(log_lik) {
	if (!is.matrix(log_lik))
	   stop('log_lik should be a matrix')
	pointwise <- pointwise_waic(log_lik)
	out <- totals(pointwise)
	nms <- names(pointwise)
	names(out) <- c(nms, paste0("se_", nms))
	out$pointwise <- cbind_list(pointwise)
	attr(out, "log_lik_dim") <- dim(log_lik)
	class(out) <- "loo"
	out
}
"""
def waic(l):
	pointwise = pointwise_waic(l)
	for k, v in pointwise.iteritems():
		yield k, total(v)

if __name__ == '__main__':
	import sys
	all_likes = []
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
		all_likes.append(l)
	all_likes = numpy.array(all_likes)
	print '%-20s : max at\tmax\tmean (log likelihood)' % 'filename'
	for i in range(len(all_likes)):
		l = all_likes[i]
		print '%-20s : %.1f%%\t%.1f\t%.1f' % (filenames[i], 
			l.argmax() * 100. / len(l),
			l.max(), l.mean()
			)
	for k, v in waic(all_likes):
		print '%-20s : %s' % (k, v)


