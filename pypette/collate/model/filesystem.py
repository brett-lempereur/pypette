"""
Generate structural observation models from structural filesystem
experiment observations.
"""

import collections
import bz2
import csv
import logging

import numpy

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.collate.model.filesystem")

def create(initial, observations):
    """
    Create a filesystem observation model.

    Arguments:
    initial -- the filename of the initial observation.
    observations -- the list of observation filenames.
    """
    # Load the set of filenames and hashes from the observations.
    il = load(initial)
    ol = map(load, observations)
    # Create the observation matrix.
    rc = len(il)
    cc = len(ol)
    arr = numpy.zeros((rc, cc), dtype=bool)
    # Construct the observation matrix.
    for i, fi in enumerate(il):
        for j, fo in enumerate(ol):
            try:
                arr[i,j] = (il[fi] == fo[fi])
            except KeyError:
                arr[i,j] = False
    return arr

def load(filename):
    """
    Load a structural filesystem observation file.

    Arguments:
    filename -- the filename of the structural filesystem observation.
    """
    container = collections.OrderedDict()
    with bz2.BZ2File(filename, "rb") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            container[row["filename"]] = row["hash"]
    return container

def identities(filename):
    """
    Load a list of filenames from an observation file.

    Arguments:
    filename -- the filename of the structural filesystem observation.
    """
    container = []
    with bz2.BZ2File(filename, "rb") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            container.append(row["filename"])
    return container
