import time
startTime = time.time() # This value will be used if we are stopping the stopwatch. If we're starting it, the value we be recalculated
import os
import sys

def usage():
    print 'Usage: python stopwatch.py [--start | --stop]'
    sys.exit(1)

FILENAME = "stopwatch_starttime.txt"
try:
    option = sys.argv[1]
except IndexError:
    usage()

if option == "--start":
    with open(FILENAME, "w") as log:
        log.write(str(time.time()))
elif option == "--stop":
    try:
        with open(FILENAME, "r") as log:
            prevTime = float(log.read())
        print "%.2f seconds" % (startTime - prevTime)
    finally:
        os.remove(FILENAME) # delete the file
else:
    usage()
