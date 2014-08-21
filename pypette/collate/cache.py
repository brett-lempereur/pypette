"""
Live digital forensic observation model cache.
"""

import logging
import os

import numpy

# The location of the observation model cache.
CACHE = r"/var/lib/pypette/cache"

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.collate.cache")

def available(situation, source, feature):
    """
    Return a list of the cached observation models for a situation
    and feature type.

    Arguments:
    situation -- the name of the live digital forensic situation.
    source -- the source of the live digital forensic observation.
    feature -- the name of the live digital forensic feature.
    """
    container = []
    try:
        path = os.path.join(CACHE, situation, source, feature)
        filenames = os.listdir(path)
        for filename in filenames:
            evaluation, extension = os.path.splitext(filename)
            container.append(evaluation)
    except OSError:
        pass
    return container

def store(situation, source, feature, evaluation, **model):
    """
    Store an observation model in the cache.

    Arguments:
    situation -- the name of the live digital forensic situation.
    source -- the source of the live digital forensic observation.
    feature -- the name of the live digital forensic feature.
    evaluation -- the name of the live digital forensic evaluation.
    model -- the observation model.
    """
    # Generate the filename for the evaluation model.
    path = os.path.join(CACHE, situation, source, feature)
    filename = os.path.join(path, "{}.npz".format(evaluation))
    # Create the necessary paths and save the model.
    if not os.path.exists(path):
        os.makedirs(path)
    numpy.savez(filename, **model)

def retrieve(situation, source, feature, evaluation):
    """
    Retrieve an observation model from the cache.

    Arguments:
    situation -- the name of the live digital forensic situation.
    source -- the source of the live digital forensic observation.
    feature -- the name of the live digital forensic feature.
    evaluation -- the name of the live digital forensic evaluation.
    """
    path = os.path.join(CACHE, situation, source, feature)
    filename = os.path.join(path, "{}.npz".format(evaluation))
    handle = numpy.load(filename)
    container = dict(handle)
    handle.close()
    return container
