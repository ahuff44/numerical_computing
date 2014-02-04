"""
    Estimates an integral using the trapezoid rule (parallel implementation)
    Example usage:
        $ mpirun -n 10 python.exe trapParallel.py 0.0 1.0 10000
    Example output:
        With 10000 trapezoids, the estimate of the integral of x^2 from 0.0 to 1.0 is:
            0.333333335
    ***In this implementation, n must be divisble by the number of processes***
"""

from __future__ import division
from sys import argv
from mpi4py import MPI
import numpy as np

def integrate_range(fxn, a, b, n):
    ''' Numerically integrates the function fxn by the trapezoid rule
        Integrates from a to b with n trapezoids
        '''
    # There are n trapezoids and therefore there are n+1 endpoints
    endpoints = np.linspace(a, b, n+1)

    integral = sum(fxn(x) for x in endpoints)
    integral -= (fxn(a) + fxn(b))/2
    integral *= (b - a)/n

    return integral

# Reading the command line arguments
a = float(argv[1])
b = float(argv[2])
n = int(argv[3])

# An arbitrary function with a well-known integral
def function(x):
    return x**2


COMM = MPI.COMM_WORLD
SIZE = COMM.Get_size()
RANK = COMM.Get_rank()

step_size = (b - a)/n
local_n = n // SIZE
# local_n is the number of trapezoids each process will calculate
# ***Remember, in this implementation, n must be divisible by SIZE***

local_a = a + RANK*local_n*step_size
local_b = local_a + local_n*step_size
# local_a and local_b are the start and end of this process' integration range

integral = np.zeros(1)
integral[0] = integrate_range(function, local_a, local_b, local_n)
# We'll be sending this through COMM.Send, so the value has to be boxed up in a numpy array

if RANK != 0:
    # Send the result to the root node. (Remember, the dest parameter defaults to 0)
    COMM.Send(integral)
else:
    # The root node now compiles and prints the results
    total = integral[0]
    recieve_buffer = np.zeros(1)
    for _ in xrange(SIZE-1):
        COMM.Recv(recieve_buffer, MPI.ANY_SOURCE)
        total += recieve_buffer[0]

    print "With {n} trapezoids, the estimate of the integral of x^2 from {a} to {b} is: \n\t{total}".format(**locals())
