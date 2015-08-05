import sys
import pystan
data = pystan.misc.read_rdump(sys.argv[1])
outfilename = sys.argv[1].rstrip('.Rdata').rstrip('.Rdump') + '.npz'
print 'storing as npz ...'
numpy.savez(outfilename, **data)

