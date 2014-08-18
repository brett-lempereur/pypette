"""
Experimental technique to sample the initial state of a virtual machine.
"""

import logging
import os
import tempfile

import pypette.emulator as emulator
import pypette.interface as interface

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.technique.initial")

class InitialStateTechnique(interface.Technique):
    """
    Sample the initial state of a virtual machine.

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
        self.image = tempfile.mktemp(".memory")

    def sample(self):
        """
        Sample the initial state of a virtual machine.
        """
        # Instantiate and revert the virtual machine to a snapshot.
        logger.info("Launching domain and reverting to snapshot")
        domain = emulator.Emulator(self.domain_host, self.domain_name)
        domain.revert(self.domain_snapshot)
        # Save an image of virtual machine memory.
        logger.info("Saving image of domain memory")
        domain.save_memory(self.image)
        # Terminate the virtual machine.
        logger.info("Terminating domain")
        domain.close()

    def release(self):
        """
        Release temporary resources.
        """
        logger.info("Unlinking memory image '%s'", self.image)
        os.unlink(self.image)

# Register the technique implementation.
interface.techniques.register("initial-state", InitialStateTechnique)

