from mpi4py import MPI
SIZE = MPI.COMM_WORLD.Get_size()
print "There are {SIZE} processes running.".format(**locals())

