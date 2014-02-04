from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()

msg_buf = np.zeros(1, dtype=int)  # This must be a numpy array
if RANK == 0:
    msg_buf[0] = 10110100
    COMM.Send(msg_buf, dest=1)
elif RANK == 1:
    COMM.Recv(msg_buf, source=0)
    print msg_buf[0]
