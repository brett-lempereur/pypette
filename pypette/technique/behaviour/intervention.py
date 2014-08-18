"""
Live digital forensic intervention behaviours.
"""

import logging

import pypette.interface as interface

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.technique.behaviour.intervention")

class ExecuteInterventionBehaviour(interface.Behaviour):
    """
    Execution live digital forensic intervention behaviour.

    Parameters:
    technique.invocation.command -- the command-line acquisition invocation.
    technique.invocation.shell -- true if the invocation requires a shell.
    technique.invocation.cwd -- the working-directory of the invocation.

    Slots:
    acquisition.standard-output -- the standard output of the invocation.
    acquisition.standard-error -- the standard error of the invocation.
    acquisition.return-code -- the return code of the information.
    """

    # Memory image acquisition invocation parameters.
    invocation_command = interface.Parameter("technique.invocation.command")
    invocation_shell = interface.Parameter("technique.invocation.shell")
    invocation_cwd = interface.Parameter("technique.invocation.cwd")

    # Acquisition invocation outputs.
    standard_output = interface.Slot("acquisition.standard-output")
    standard_error = interface.Slot("acquisition.standard-error")
    return_code = interface.Slot("acquisition.return-code")

    def acquire(self, domain, agent):
        """
        Acquire live digital forensic evidence by intervening in the
        execution of the domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        reply = agent.execute(
            self.invocation_command,
            self.invocation_shell,
            self.invocation_cwd
        )
        self.standard_output = reply["stdout"]
        self.standard_error = reply["stderr"]
        self.return_code = reply["return_code"]

class MonitorInterventionBehaviour(interface.Behaviour):
    """
    Monitoring live digital forensic intervention behaviour.

    Parameters:
    technique.invocation.command -- the command-line acquisition invocation.
    technique.invocation.interval -- the invocation sampling interval.
    technique.invocation.cwd -- the working-directory of the invocation.

    Slots:
    acquisition.samples -- the performance samples of the invocation.
    acquisition.standard-output -- the standard output of the invocation.
    acquisition.standard-error -- the standard error of the invocation.
    acquisition.return-code -- the return code of the information.
    """

    # Memory image acquisition invocation parameters.
    invocation_command = interface.Parameter("technique.invocation.command")
    invocation_interval = interface.Parameter("technique.invocation.interval")
    invocation_cwd = interface.Parameter("technique.invocation.cwd")

    # Acquisition invocation outputs.
    samples = interface.Slot("acquisition.samples")
    standard_output = interface.Slot("acquisition.standard-output")
    standard_error = interface.Slot("acquisition.standard-error")
    return_code = interface.Slot("acquisition.return-code")

    def acquire(self, domain, agent):
        """
        Acquire live digital forensic evidence by intervening in the
        execution of the domain and sampling the performance of the
        acquisition technique.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        reply = agent.monitor(
            self.invocation_command,
            self.invocation_interval,
            self.invocation_cwd
        )
        self.samples = reply["samples"]
        self.standard_output = reply["stdout"]
        self.standard_error = reply["stderr"]
        self.return_code = reply["return_code"]
