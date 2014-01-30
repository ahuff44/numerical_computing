from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

print "Hello world! I'm process number {RANK} out of {SIZE}.".format(**locals())
# See http://docs.python.org/2/library/string.html#formatstrings if this syntax for string formatting is unfamiliar
