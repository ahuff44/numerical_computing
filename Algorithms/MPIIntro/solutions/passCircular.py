'''
See \ref{prob:MPI_Intro:passCircular.py}

Many processes each passing a random number to their neighbor process
Usage:
    $ mpirun -n 5 python.exe passCircular.py
'''
from sys import argv
import numpy as np
from mpi4py import MPI

COMM = MPI.COMM_WORLD
SIZE = COMM.Get_size()
RANK = COMM.Get_rank()

rank_to_recieve_from = RANK - 1 if RANK - 1 >= 0 else SIZE-1
rank_to_send_to = RANK + 1 if RANK + 1 < SIZE else 0

# Send the message
send_buffer = np.random.rand(1)
print "Process {RANK}: Sending {send_buffer}".format(**locals())
COMM.Send(send_buffer, dest=rank_to_send_to)

# Recieve a message
recieve_buffer = np.zeros(1)
print "Process {RANK}: Waiting for message; recieve_buffer={recieve_buffer}".format(**locals())
COMM.Recv(recieve_buffer, source=rank_to_recieve_from)
print "Process {RANK}: Recieved {recieve_buffer}".format(**locals())
