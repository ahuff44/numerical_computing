import numpy as np
from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()

if RANK == 1:  # This process chooses and sends a random value
    send_buffer = np.random.rand(1)
    # Note that send_buffer is a numpy array.
    # MPI requires messages to be sent as nunpy arrays

    print "Process 1: Sending: {send_buffer} to process 0.".format(**locals())
    COMM.Send(send_buffer, dest=0)
    print "Process 1: Message sent."
if RANK == 0:  # This process recieves a value from process 1
    receive_buffer = np.zeros(1)
    # Again, note that this receive_buffer is a numpy array

    print "Process 0: Waiting for the message... current receive_buffer={receive_buffer}.".format(**locals())
    COMM.Recv(receive_buffer, source=1)
    print "Process 0: Message recieved! receive_buffer={receive_buffer}.".format(**locals())
