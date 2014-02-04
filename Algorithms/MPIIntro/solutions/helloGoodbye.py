'''
See \ref{prob:MPI_Intro:helloGoodbye.py}

Exercise solution: Prints a message that depends on process rank
Usage:
    >>> mpirun -n 8 python.exe helloGoodbye.py
'''
from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()

rank_is_odd = bool(RANK % 2)
if rank_is_odd:
    print "Hello from process {RANK}!".format(**locals())
else:
    print "Goodbye from process {RANK}.".format(**locals())
