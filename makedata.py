import numpy
from numpy import sin, pi, log10, exp

phi = 0.3
T = 0.1
A = 2
SNR = 1
noise = SNR * A
numpy.random.seed(1)

N = 40
t = numpy.linspace(0, 1, N)
y = A * sin(2*pi * (t/T + phi))

yobs = numpy.random.normal(y, noise)

numpy.savez('data.npz', yobs=yobs, t=t, N=N)



