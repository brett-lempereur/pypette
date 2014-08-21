"""
Generate structural observation models from logical memory page experiment
observations.
"""

import bz2
import collections
import csv
import logging

import numpy

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.collate.model.page")

def create(initial, observations):
    """
    Create a logical memory page observation model.

    Arguments:
    initial -- the filename of the initial observation.
    observations -- the list of observation filenames.
    """
    # Load the logical page observations.
    il = load(initial)
    ol = map(load, observations)
    # Create the observation matrix.
    rc = len(il)
    cc = len(ol)
    arr = numpy.zeros((rc, cc), dtype=bool)
    # Construct the observation matrix.
    for i, pi in enumerate(il):
        for j, po in enumerate(ol):
            try:
                arr[i,j] = (il[pi] == po[pi])
            except KeyError:
                arr[i,j] = False
    return arr

def load(filename):
    """
    Load a logical page observation file.

    Arguments:
    filename -- the filename of the logical page observation.
    """
    container = collections.OrderedDict()
    with bz2.BZ2File(filename, "rb") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            offset = int(row["offset"], 16)
            size = int(row["size"], 16)
            container[(offset, size)] = row["checksum"]
    return container
