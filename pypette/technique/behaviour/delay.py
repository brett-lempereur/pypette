"""
Live digital forensic experiment delay behaviours.
"""

import logging
import random
import time

import pypette.interface as interface

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.technique.behaviour.delay")

class FixedDelayBehaviour(interface.Behaviour):
    """
    Fixed live digital forensic experiment delay behaviour.

    Parameters:
    technique.duration -- the number of seconds to idle the virtual machine.
    """

    # Delay parameters.
    duration = interface.Parameter("technique.duration")

    def idle(self):
        """
        Allow the live digital forensic situation to execute without
        interaction for a fixed period.
        """
        logger.info("Idling virtual machine for %d seconds", self.duration)
        time.sleep(self.duration)

class RandomDelayBehaviour(interface.Behaviour):
    """
    Random live digital forensic experiment delay behaviour.

    Parameters:
    technique.duration.mean -- the mean duration to idle the virtual machine.
    technique.duration.stdev -- the standard deviation of the duration.
    """

    # Delay parameters.
    mean = interface.Parameter("technique.duration.mean")
    stdev = interface.Parameter("technique.duration.stdev")

    def idle(self):
        """
        Allow the live digital forensic situation to execute without
        interaction for a period drawn from a normal distribution.
        """
        duration = random.normalvariate(self.mean, self.stdev)
        logger.info("Idling virtual machine for %d seconds", duration)
        time.sleep(duration)
