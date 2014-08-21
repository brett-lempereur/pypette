"""
Generate semantic observation models from volatile semantic experiment
observations.
"""

import bz2
import collections
import csv
import logging

import numpy

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.collate.model.semantic")

def create(initial, observations, fields):
    """
    Create a semantic observation model.

    Arguments:
    initial -- the filename of the initial observation.
    observations -- the list of observation filenames.
    fields -- the list of semantic feature identifier fields.
    """
    # WARNING: We use a sorted list for the initial set to guarauntee that
    # the semantic features will always be ordered, but keep the observations
    # in sets to preserve the efficiency of the loop.
    il = sorted(extract(load(initial), fields))
    ol = [extract(load(fn), fields) for fn in observations]
    # Create the observation matrix.
    rc = len(il)
    cc = len(ol)
    arr = numpy.zeros((rc, cc), dtype=bool)
    # Construct the observation matrix.
    for i, iv in enumerate(il):
        for j, ov in enumerate(ol):
            arr[i,j] = (iv in ov)
    return arr

def load(filename):
    """
    Load a volatile semantic observation file.

    Arguments:
    filename -- the filename of the volatile semantic observation.
    """
    container = []
    with bz2.BZ2File(filename, "rb") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader]

def extract(observation, fields):
    """
    Extract a set of unique semantic features.

    Arguments:
    observation -- the volatile semantic observation.
    fields -- the list of semantic feature identifier fields.
    """
    container = set()
    for feature in observation:
        description = tuple(feature[field] for field in fields)
        container.add(description)
    return container

def identities(observation, fields):
    """
    Extract a list of unique semantic features and their descriptions.

    Arguments:
    observation -- the volatile semantic observation.
    fields -- the list of semantic feature identifier fields.
    """
    container = set()
    for feature in observation:
        description = tuple(feature[field] for field in fields)
        container.add(description)
    return sorted(container)
