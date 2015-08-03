Information criteria for Stan
==============================

* ic.py -- computes various information criteria, including

  * AIC  (Akaike 1974)
  * AICc (Cavanaugh 1997)
  * DIC (Spiegelhalter+2004)
  * DIC (Gelman+2004)
  * BIC (Schwarz 1978)
  * WAIC (Watanabe 2010)
  * TODO: WBIC (Watanabe 2013) (help appreciated!)

* csv2Rdata.py -- start a Stan run where another terminated (e.g. optimize, then sample)

Example
----------

* run.sh -- generate data and compute chains
* ic.py chain?.npz -- compute the information criteria::

	chain1.npz           | maxlike    | -53.6
	chain1.npz           | elpd_waic  | -48.9
	chain1.npz           | waic       | 97.9
	chain1.npz           | p_waic     | 2.6
	chain1.npz           | dic        | 118.3
	chain1.npz           | dic_gelman | 119.2
	chain1.npz           | aic        | 123.2

	chain2.npz           | maxlike    | -53.5
	chain2.npz           | elpd_waic  | -48.9
	chain2.npz           | waic       | 97.8
	chain2.npz           | p_waic     | 2.6
	chain2.npz           | dic        | 118.0
	chain2.npz           | dic_gelman | 119.1
	chain2.npz           | aic        | 123.1

	[...]

	criterion  : mean	std
	maxlike    : -53.0	0.8
	elpd_waic  : -49.0	0.2
	waic       : 98.0	0.4
	p_waic     : 2.9	0.3
	dic        : 118.2	0.3
	dic_gelman : 119.7	0.5
	aic        : 121.9	1.7




