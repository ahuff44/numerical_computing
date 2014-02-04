"""
    Demonstrates some timing concerns with the parallel implementation of the trapezoid rule
    Example usage:
        $ mpirun -n 4 python.exe trapSpeedDemo.py
    ***In this implementation, the number of processes must divide 48***
"""
from __future__ import division
from sys import argv
from mpi4py import MPI
import numpy as np
import time

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
a = 0.0
b = 1.0
n = 48

# An arbitrary function with a well-known integral
# We're artificially making this function call very expensive
def expensiveFunction(x):
    time.sleep(0.01)
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
integral[0] = integrate_range(expensiveFunction, local_a, local_b, local_n)
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

    # print "With {n} trapezoids, the estimate of the integral of x^2 from {a} to {b} is: \n\t{total}".format(**locals())
