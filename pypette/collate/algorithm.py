"""
General-purpose algorithms for processing observation models.
"""

import logging

import numpy
import uncertainties

import pypette.collate.measure as measure

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.collate.algorithm")

def feature_absolute_error(sx):
    """
    Return a pair of vectors that contain the mean absolute error and
    standard error of the mean absolute error for each feature in an
    observation model.

    Arguments:
    sx -- the observation model.
    """
    n = sx.shape[0]
    mu = numpy.ndarray(n, dtype=float)
    sigma = numpy.ndarray(n, dtype=float)
    for i in numpy.arange(0, n):
        err = measure.absolute_error(sx[i:i+1])
        mu[i] = uncertainties.nominal_value(err)
        sigma[i] = uncertainties.std_dev(err)
    return mu, sigma

def feature_relative_error(sx):
    """
    Return a pair of vectors that contain the mean relative error and
    standard error of the mean relative error for each feature in an
    observation model.

    Arguments:
    sx -- the observation model.
    """
    n = sx.shape[0]
    mu = numpy.ndarray(n, dtype=float)
    sigma = numpy.ndarray(n, dtype=float)
    for i in numpy.arange(0, n):
        err = measure.relative_error(sx[i:i+1])
        mu[i] = uncertainties.nominal_value(err)
        sigma[i] = uncertainties.std_dev(err)
    return mu, sigma

def feature_attributable_risk(sx, sy):
    """
    Return a pair of vectors that contain the attributable risk and the
    standard error of the attributable risk for each feature between an
    exposed and unexposed group.

    Arguments:
    sx -- the observation model of the exposed group.
    sy -- the observation model of the unexposed group.
    """
    if sx.shape[0] != sy.shape[0]:
        raise ValueError("Observation models must have same number of rows")
    n = sx.shape[0]
    mu = numpy.ndarray(n, dtype=float)
    sigma = numpy.ndarray(n, dtype=float)
    for i in numpy.arange(0, n):
        ar = measure.attributable_risk(sx[i:i+1], sy[i:i+1])
        mu[i] = uncertainties.nominal_value(ar)
        sigma[i] = uncertainties.std_dev(ar)
    return mu, sigma

def feature_relative_risk(sx, sy):
    """
    Return a pair of vectors that contain the relative risk and the
    standard error of the relative risk for each feature between an
    exposed and unexposed group.

    Arguments:
    sx -- the observation model of the exposed group.
    sy -- the observation model of the unexposed group.
    """
    if sx.shape[0] != sy.shape[0]:
        raise ValueError("Observation models must have same number of rows")
    n = sx.shape[0]
    mu = numpy.ndarray(n, dtype=float)
    sigma = numpy.ndarray(n, dtype=float)
    for i in numpy.arange(0, n):
        ar = measure.relative_risk(sx[i:i+1], sy[i:i+1])
        mu[i] = uncertainties.nominal_value(ar)
        sigma[i] = uncertainties.std_dev(ar)
    return mu, sigma

def above_threshold(vx, theta):
    """
    Return a list of indices in a feature measure vector where values are
    greater than or equal to a threshold.

    Arguments:
    vx -- the vector of feature-level measures.
    theta -- the threshold value.
    """
    container = []
    for i in numpy.arange(0, vx.shape[0]):
        if vx[i] >= theta:
            container.append(i)
    return container

def below_threshold(vx, theta):
    """
    Return a list of indices in a feature measure vector where values are
    less than or equal to a threshold.

    Arguments:
    vx -- the vector of feature-level measures.
    theta -- the threshold value.
    """
    container = []
    for i in numpy.arange(0, vx.shape[0]):
        if vx[i] <= theta:
            container.append(i)
    return container
