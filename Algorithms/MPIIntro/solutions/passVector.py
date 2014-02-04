'''
See \ref{prob:MPI_Intro:passVector.py}

Passing a random vector between two processes
Usage:
    $ mpirun -n 2 python.exe passVector.py 6

arguments: n, the length of the vector to pass between the nodes
'''
from sys import argv
import numpy as np
from mpi4py import MPI

COMM = MPI.COMM_WORLD
SIZE = COMM.Get_size()
RANK = COMM.Get_rank()

# the length of the vector to pass:
if len(argv) != 2:
    print "Example usage: >>> mpirun -n 2 python.exe passVector.py 6"
    COMM.Abort()
n = int(argv[1])


if RANK == 0:
    # Generate and send a random array to the other process
    send_buffer = np.random.rand(n)
    print "Process {RANK}: Sending: send_buffer={send_buffer}".format(**locals())
    COMM.Send(send_buffer, dest=1)
elif RANK == 1:
    # Prepare and recieve the array from the root process
    recieve_buffer = np.zeros(n)
    print "Process {RANK}: Waiting for message; recieve_buffer={recieve_buffer}".format(**locals())
    COMM.Recv(recieve_buffer)
    print "Process {RANK}: Recieved: recieve_buffer={recieve_buffer}".format(**locals())
