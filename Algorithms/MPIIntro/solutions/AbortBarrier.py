'''
See \ref{prob:MPI_Intro:AbortBarrier.py}

Only runs when there are 5 processes
>>> mpirun -n 5 python.exe AbortBarrier.py
'''
from mpi4py import MPI

COMM = MPI.COMM_WORLD
SIZE = COMM.Get_size()
RANK = COMM.Get_rank()

if RANK == 0 and SIZE != 5:
    print "Error: This program must run with exactly 5 processes."
    COMM.Abort()
COMM.Barrier()
print "Success!"
