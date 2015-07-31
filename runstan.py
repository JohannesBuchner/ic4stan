import json
import numpy
import os
import sys
import pickle
from numpy import exp, log, log10
import pystan
import logging

model_code = open(sys.argv[2]).read()

logger = logging.getLogger('pystan')

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

print 'creating model ...'
try:
	model = pickle.load(open(sys.argv[2] + '.pkl', 'rb'))
except IOError, EOFError:
	model = pystan.StanModel(model_code=model_code, save_dso=True, verbose=True)
	with open(sys.argv[2] + '.pkl', 'wb') as f:
		pickle.dump(model, f)

print 'creating model done.'

print 'loading data ...'
data = dict(numpy.load(sys.argv[1]))
print 'sampling ...'
fit = model.sampling(data=data,
	iter=20000, warmup=1000, chains=1, n_jobs=-1,
	verbose=True, refresh=50,
	)
la = fit.extract(permuted=True)

print 'saving...'
numpy.savez(sys.argv[3], **la)


