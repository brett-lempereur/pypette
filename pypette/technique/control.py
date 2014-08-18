"""
Live digital forensic experimental control techniques.
"""

import logging
import os
import tempfile

import pypette.emulator as emulator
import pypette.interface as interface

# The experimental parameter that specifies which delay behaviour to
# use in a control experiment.
DELAY_BEHAVIOUR_KEY = "technique.behaviour.delay"

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.technique.control")

class ControlTechnique(interface.Technique):
    """
    Live digital forensic control experiment technique.

    Parameters:
    technique.domain.host -- the address of the virtualisation platform.
    technique.domain.name -- the name of the virtual machine domain.
    technique.domain.snapshot -- the name of the virtual machine snapshot.

    Slots:
    memory.image -- the virtual machine memory image.
    """

    # Virtual machine domain parameters.
    domain_host = interface.Parameter("technique.domain.host")
    domain_name = interface.Parameter("technique.domain.name")
    domain_snapshot = interface.Parameter("technique.domain.snapshot")

    # Memory image slots.
    image = interface.Slot("memory.image")

    def allocate(self):
        """
        Allocate temporary resources.
        """
        logger.info("Allocating file for memory image")
        self.image = tempfile.mktemp(".memory")

    def sample(self):
        """
        Collect a control sample from a live digital forensic situation.
        """
        # Instantiate and revert the virtual machine to a snapshot.
        logger.info("Launching domain and reverting to snapshot")
        domain = emulator.Emulator(self.domain_host, self.domain_name)
        try:
            domain.revert(self.domain_snapshot)
            # Execute the machine and allow it to idle.
            logger.info("Executing domain without user-interaction")
            domain.resume()
            self.idle()
            # Save an image of virtual machine memory.
            logger.info("Saving image of domain memory")
            domain.suspend()
            domain.save_memory(self.image)
            # Terminate the virtual machine.
            logger.info("Terminating domain")
        finally:
            domain.close()

    def idle(self):
        """
        Allow the live digital forensic situation to execute without
        interaction for some period.
        """
        raise NotImplementedError()

    def release(self):
        """
        Release temporary resources.
        """
        logger.info("Unlinking memory image '%s'", self.image)
        if os.path.exists(self.image):
            os.unlink(self.image)

def control_technique_factory(parameters):
    """
    Return a class that implements the requested control technique
    behaviour.

    Parameters:
    parameters -- the technique parameter dictionary.
    """
    # Load the delay behaviour module when needed to avoid a circular
    # dependency problem when loading this module.
    import pypette.technique.behaviour.delay as delay
    DELAY_BEHAVIOURS = {
        "fixed": delay.FixedDelayBehaviour,
        "random": delay.RandomDelayBehaviour
    }
    # If possible, construct a technique implementation using the selected
    # behaviours.
    try:
        db = DELAY_BEHAVIOURS[parameters[DELAY_BEHAVIOUR_KEY]]
    except KeyError:
        raise RuntimeError("Requested behaviour could not be composed")
    inheritance = (db, ControlTechnique,)
    klass = type("DynamicControlTechnique", inheritance, {})
    return klass(parameters)

# Register the dynamic control technique factory.
interface.techniques.register("control", control_technique_factory)
