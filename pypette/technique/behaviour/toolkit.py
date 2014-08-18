"""
Live digital forensic acquisition toolkit behaviours.
"""

import logging

import pypette.interface as interface

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.technique.behaviour.toolkit")

class OpticalAcquisitionToolkit(interface.Behaviour):
    """
    Optical live digital forensic toolkit behaviour.

    Parameters:
    technique.toolkit.image -- the path of the toolkit image.
    technique.toolkit.device -- the device on which to attach the toolkit.
    technique.toolkit.tag -- the identification tag of the toolkit.
    """

    # Optical acquisition toolkit parameters.
    toolkit_image = interface.Parameter("technique.toolkit.image")
    toolkit_device = interface.Parameter("technique.toolkit.device")
    toolkit_tag = interface.Parameter("technique.toolkit.tag")

    def attach_toolkit(self, domain, agent):
        """
        Attach the optical live digital forensic acquisition toolkit to
        the domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        logger.info("Attaching optical acquisition toolkit to domain")
        domain.change_optical(self.toolkit_device, self.toolkit_image)
        agent.find(self.toolkit_tag)

    def detach_toolkit(self, domain, agent):
        """
        Detach the optical live digital forensic acquisition toolkit
        from the domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        logger.info("Detaching optical acquisition toolkit from domain")
        domain.eject_optical(self.toolkit_device)
