"""
Visualise measures of live digital forensic observation models.
"""

import logging

import matplotlib.cm
import matplotlib.pyplot
import matplotlib.ticker as ticker
import numpy

import pypette.collate.algorithm

# Colour schemes for the error and risk bitmaps.
ERROR_SCHEME = matplotlib.cm.hot
RISK_MEAN_SCHEME = matplotlib.cm.seismic
RISK_SE_SCHEME = matplotlib.cm.gray_r

# Interpolation method.
INTERPOLATION = "nearest"

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.collate.visualise")

def error_bitmap(sx, mu_axes, sigma_axes):
    """
    Plot bitmaps of the mean relative error and standard deviation of the
    mean relative error.

    Arguments:
    sx -- the observation model.
    mu_axes -- the axis of the mean relative error bitmap.
    sigma_axes -- the axis of the mean relative error standard deviation bitmap.
    cmap -- the colour map of the bitmap.
    """
    # Construct the mean and sigma matrices.
    mu_v, sigma_v = analysis.algorithm.feature_relative_error(sx)
    mu_m, sigma_m = square(mu_v), square(sigma_v)
    # Plot the mean relative error bitmap.
    mu_axes.get_xaxis().set_major_locator(ticker.NullLocator())
    mu_axes.get_yaxis().set_major_locator(ticker.NullLocator())
    mu_im = mu_axes.imshow(mu_m, vmin=0, vmax=1, cmap=ERROR_SCHEME)
    mu_im.set_interpolation(INTERPOLATION)
    # Plot the mean relative error standard deviation bitmap.
    sigma_axes.get_xaxis().set_major_locator(ticker.NullLocator())
    sigma_axes.get_yaxis().set_major_locator(ticker.NullLocator())
    sigma_im = sigma_axes.imshow(sigma_m, vmin=0, vmax=1, cmap=ERROR_SCHEME)
    sigma_im.set_interpolation(INTERPOLATION)
    # Return the mean and relative error images for colour bar plotting.
    return mu_im, sigma_im

def risk_bitmap(sx, sy, mu_axes, sigma_axes):
    """
    Plot bitmaps of the mean attributable risk and standard deviation of
    the mean attributable risk.

    Arguments:
    sx -- the observation model of the exposed group.
    sy -- the observation model of the unexposed group.
    mu_axes -- the axes of the mean relative error bitmap.
    sigma_axes -- the axes of the standard deviation mean relative error bitmap.
    cmap -- the colour map of the bitmap.
    """
    # Construct the mean and sigma matrices.
    mu_v, sigma_v = analysis.algorithm.feature_attributable_risk(sx, sy)
    mu_m, sigma_m = square(mu_v), square(sigma_v)
    # Plot the mean relative error bitmap.
    mu_axes.get_xaxis().set_major_locator(ticker.NullLocator())
    mu_axes.get_yaxis().set_major_locator(ticker.NullLocator())
    mu_im = mu_axes.imshow(mu_m, vmin=-1, vmax=1, cmap=RISK_MEAN_SCHEME)
    mu_im.set_interpolation(INTERPOLATION)
    # Plot the mean relative error standard deviation bitmap.
    sigma_axes.get_xaxis().set_major_locator(ticker.NullLocator())
    sigma_axes.get_yaxis().set_major_locator(ticker.NullLocator())
    sigma_im = sigma_axes.imshow(sigma_m, vmin=0, vmax=0.25, cmap=RISK_SE_SCHEME)
    sigma_im.set_interpolation(INTERPOLATION)
    # Return the mean and relative error images for colour bar plotting.
    return mu_im, sigma_im

def square(vx):
    """
    Find a square two-dimensional matrix that is large enough to contain the
    values in a vector.

    Arguments:
    vx -- the measure vector.
    """
    logger.info("Starting brute-force algorithm to find square matrix")
    v = vx
    n = numpy.sqrt(len(v))
    i = 0
    while not n.is_integer():
        i += 1
        v = numpy.append(v, 0.0)
        n = numpy.sqrt(len(v))
    logger.info("Brute-furce algorithm added %d elements to vector", i)
    print "Brute force dimension:", n, "opposed to", numpy.ceil(numpy.sqrt(len(vx)))
    return v.reshape((n, n))
