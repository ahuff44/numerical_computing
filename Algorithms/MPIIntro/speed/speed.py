"""
    Takes the norm of a random vector
    TODO make vector constant size- 48 probs
"""
from mpi4py import MPI
import time
import numpy as np

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

STEP_SIZE = 1

def expensiveFunction(subvec):
    time.sleep(0.1)
    return sum(x**2 for x in subvec)

if RANK == 0:
    vector = np.random.rand(SIZE-1) #todo
    # Send
    for dest in xrange(1, SIZE):
        send_buffer = np.array(vector[dest-1:dest]) # TODO include STEP_SIZE
        COMM.Send(send_buffer, dest=dest)
    # Gather
    total = 0
    for _ in xrange(1, SIZE):
        recv_buffer = np.zeros(1)
        COMM.Recv(recv_buffer, source=MPI.ANY_SOURCE)
        total += recv_buffer[0]
    print "{vector}.norm() =: {total}".format(**locals())
    print "par/ser discrepancy:", total - sum(x**2 for x in vector)
    # print "ser:", sum(x**2 for x in vector)
else:
    recv_buf = np.zeros(STEP_SIZE)
    COMM.Recv(recv_buf)
    send_buf = np.zeros(1)
    send_buf[0] = expensiveFunction(recv_buf)
    COMM.Send(send_buf)
