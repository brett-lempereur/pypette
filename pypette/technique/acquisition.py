"""
Live digital forensic memory acquisition techniques.
"""

import logging
import os
import tempfile
import time

import pypette.agent
import pypette.emulator as emulator
import pypette.interface as interface

# The experiment parameters that specify which acquisition toolkit and
# vector behaviours to use.
TOOLKIT_BEHAVIOUR_KEY = "technique.behaviour.toolkit"
VECTOR_BEHAVIOUR_KEY = "technique.behaviour.vector"
INTERVENTION_BEHAVIOUR_KEY = "technique.behaviour.intervention"

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.technique.acquisition")

class AcquisitionTechnique(interface.Technique):
    """
    Abstract live digital forensic memory acquisition technique.

    Parameters:
    technique.domain.host -- the address of the virtualisation platform.
    technique.domain.name -- the name of the virtual machine domain.
    technique.domain.snapshot -- the name of the virtual machine snapshot.
    technique.domain.agent -- the address of the virtual machine guest agent.

    Slots:
    memory.final -- the final virtual machine state memory image.
    agent.initial -- the initial guest agent performance sample.
    agent.final -- the final guest agent performance sample.
    time.sample.start -- the time at which sampling started.
    time.sample.finish -- the time at which sampling finished.
    time.acquisition.start -- the time at which acquisition started.
    time.acquisition.finish -- the time at which acquisition finished.
    """

    # Virtual machine domain parameters.
    domain_host = interface.Parameter("technique.domain.host")
    domain_name = interface.Parameter("technique.domain.name")
    domain_snapshot = interface.Parameter("technique.domain.snapshot")
    domain_agent = interface.Parameter("technique.domain.agent")

    # Memory image slots.
    image_final = interface.Slot("memory.final")

    # Guest agent performance slots.
    agent_initial = interface.Slot("agent.initial")
    agent_final = interface.Slot("agent.final")

    # Timing information slots.
    sample_start = interface.Slot("time.sample.start")
    sample_finish = interface.Slot("time.sample.finish")
    acquisition_start = interface.Slot("time.acquisition.start")
    acquisition_finish = interface.Slot("time.acquisition.finish")

    def allocate(self):
        """
        Allocate temporary resources.
        """
        logger.info("Allocating resources")
        self.image_final = tempfile.mktemp(".memory")
        self.allocate_behaviour()

    def sample(self):
        """
        Sample the effects of a live digital forensic memory acquisition
        intervention on a virtual machine.
        """
        self.sample_start = time.time()
        logger.info("Launching domain and reverting to snapshot")
        domain = emulator.Emulator(self.domain_host, self.domain_name)
        try:
            domain.revert(self.domain_snapshot)
            logger.info("Connecting to the virtual machine guest agent")
            agent = pypette.agent.Agent(self.domain_agent)
            self.acquisition_start = time.time()
            logger.info("Attaching acquisition toolkit and vector")
            domain.resume()
            self.agent_initial = agent.status()
            self.attach_toolkit(domain, agent)
            self.attach_vector(domain, agent)
            logger.info("Launching the live digital forensic acquisition")
            self.acquire(domain, agent)
            logger.info("Detaching acquisition toolkit and vector")
            self.detach_toolkit(domain, agent)
            self.detach_vector(domain, agent)
            self.acquisition_finish = time.time()
            self.agent_final = agent.status()
            logger.info("Collecting final memory image and terminating domain")
            domain.suspend()
            domain.save_memory(self.image_final)
        finally:
            domain.close()
        logger.info("Transferring the acquired memory image to the host")
        self.transfer_acquired_image()
        self.sample_finish = time.time()

    def attach_toolkit(self, domain, agent):
        """
        Attach the live digital forensic acquisition toolkit to the
        domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        raise NotImplementedError()

    def detach_toolkit(self, domain, agent):
        """
        Detach the live digital forensic acquisition toolkit from the
        domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        raise NotImplementedError()

    def attach_vector(self, domain, agent):
        """
        Attach the live digital forensic acquisition vector to the
        domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        raise NotImplementedError()

    def acquire(self, domain, agent):
        """
        Acquire live digital forensic evidence by intervening in the
        execution of the domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        pass

    def detach_vector(self, domain, agent):
        """
        Detach the live digital forensic acquisition vector from the
        domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        raise NotImplementedError()

    def transfer_acquired_image(self):
        """
        Transfer the acquired memory image from the acquisition vector
        to the host machine.
        """
        raise NotImplementedError()

    def release(self):
        """
        Release temporary resources.
        """
        logger.info("Releasing resources")
        if os.path.exists(self.image_final):
            os.unlink(self.image_final)
        self.release_behaviour()

def acquisition_technique_factory(parameters):
    """
    Return a class that implements the requested acquisition technique
    behaviour.

    Parameters:
    parameters -- the technique parameter dictionary.
    """
    # Load the behaviour modules and define the available behaviours for
    # the acquisition technique.  We have to do this inside this method
    # to avoid circular import dependencies.
    import pypette.technique.behaviour.intervention as intervention
    import pypette.technique.behaviour.toolkit as toolkit
    import pypette.technique.behaviour.vector as vector 
    TOOLKIT_BEHAVIOURS = {
        "optical": toolkit.OpticalAcquisitionToolkit
    }
    VECTOR_BEHAVIOURS = {
        "fixed-drive": vector.FixedDriveAcquisitionVector
    }
    INTERVENTION_BEHAVIOURS = {
        "execute": intervention.ExecuteInterventionBehaviour,
        "monitor": intervention.MonitorInterventionBehaviour
    }
    # If possible, construct a technique implementation using the selected
    # behaviours.
    try:
        tkb = TOOLKIT_BEHAVIOURS[parameters[TOOLKIT_BEHAVIOUR_KEY]]
        vcb = VECTOR_BEHAVIOURS[parameters[VECTOR_BEHAVIOUR_KEY]]
        ivb = INTERVENTION_BEHAVIOURS[parameters[INTERVENTION_BEHAVIOUR_KEY]]
    except KeyError:
        raise RuntimeError("Requested behaviour could not be composed")
    inheritance = (ivb, tkb, vcb, AcquisitionTechnique,)
    klass = type("DynamicAcquisitionTechnique", inheritance, {})
    return klass(parameters)

# Register the dynamic acquisition technique factory.
interface.techniques.register("acquisition", acquisition_technique_factory)

