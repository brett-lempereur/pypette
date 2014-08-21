"""
Calculate measures of live digital forensic observation models.
"""

import logging

import numpy
import uncertainties

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.collate.measure")

def absolute_error(sx):
    """
    Return the absolute error of an observation.

    Arguments:
    sx -- the observation model.
    """
    v = absolute_error_vector(sx)
    kx = sx.shape[1]
    mu = numpy.mean(v)
    sigma = numpy.std(v) / numpy.sqrt(kx)
    return uncertainties.ufloat((mu, sigma,))

def absolute_error_vector(sx):
    """
    Return a vector of the absolute errors of each execution in an
    observation.

    Arguments:
    sx -- the observation model.
    """
    n = sx.shape[0]
    t = numpy.sum(sx, axis=0)
    return n - t

def relative_error(sx):
    """
    Return the relative error of an observation.

    Arguments:
    sx -- the observation model.
    """
    v = relative_error_vector(sx)
    kx = sx.shape[1]
    mu = numpy.mean(v)
    sigma = numpy.std(v) / numpy.sqrt(kx)
    return uncertainties.ufloat((mu, sigma,))

def relative_error_vector(sx):
    """
    Return a vector of the relative errors of each execution in an
    observation.

    Arguments:
    sx -- the observation model.
    """
    n = sx.shape[0]
    e = absolute_error_vector(sx)
    return e / float(n)

def attributable_risk(sx, sy):
    """
    Return the attributable risk calculated as the difference in
    proportion of errors between an exposed and unexposed group.

    Arguments:
    sx -- the observation model of the exposed group.
    sy -- the observation model of the unexposed group.
    """
    ex = relative_error(sx)
    ey = relative_error(sy)
    return ex - ey
