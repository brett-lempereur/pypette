"""
Generate structural observation models from physical structural experiment
observations.
"""

import bz2
import logging

import numpy

# The number of bytes in a physical observation file quantum.
QUANTUM_BYTES = 33

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.collate.physical")

def create(initial, observations):
    """
    Create a physical observation model.

    Arguments:
    initial -- the filename of the initial observation.
    observations -- the list of observation filenames.
    """
    # Create the observation matrix.
    rc = quantum_count(initial)
    cc = len(observations)
    arr = numpy.zeros((rc, cc), dtype=bool)
    # Open the file handles.
    ih = bz2.BZ2File(initial, "r", buffering=4096)
    oh = [bz2.BZ2File(fn, "r", buffering=4096) for fn in observations]
    # Construct the observation matrix.
    for i in xrange(0, rc):
        iv = ih.readline()
        for j, h in enumerate(oh):
            ov = h.readline()
            arr[i,j] = (ov == iv)
    return arr

def quantum_count(filename):
    """
    Determine the quantum count in a physical observation file.

    Arguments:
    filename -- the filename of the structural observation.
    """
    with bz2.BZ2File(filename, "r") as handle:
        handle.seek(0, 2)
        return handle.tell() / QUANTUM_BYTES

