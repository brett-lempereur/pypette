"""
Static and slot-based file compression digital forensic analysts.
"""

import logging
import os
import subprocess

import pypette.interface as interface

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.analyst.compress")

def compress(source, target):
    """
    Compress a file.

    Arguments:
    source -- the filename of the source.
    target -- the filename of the target.
    """
    with open(target, "wb") as handle:
        subprocess.check_call(["pbzip2", "-c", source], stdout=handle)

class CompressSlotAnalyst(interface.Analyst):
    """
    Slot-based file compression digital forensic analyst.

    Parameters:
    analyst.compress-slot.slot -- the name of the slot.
    analyst.compress-slot.output -- the name of the output file.
    """
    
    # Slot-based compression parameters.
    slot = interface.Parameter("analyst.compress-slot.slot")
    output = interface.Parameter("analyst.compress-slot.output")

    def analyse(self, execution, sample):
        """
        Compress the file referenced in a sample slot.
        """
        source = sample[self.slot]
        target = self.output.format(execution=execution)
        logger.info("Compressing '%s' to '%s'", source, target)
        compress(source, target)
    
    def discard(self, execution):
        """
        Discard the compressed file.
        """
        target = self.output.format(execution=execution)
        try:
            os.unlink(target)
        except OSError:
            # The file does not exist, this error is expected and can be
            # safely ignored.
            pass

class CompressFileAnalyst(interface.Analyst):
    """
    File compression digital forensic analyst.

    Parameters:
    analyst.compress-file.filename -- the name of the file to compress.
    analyst.compress-file.output -- the name of the output file.
    """

    # File-based compression parameters.
    filename = interface.Parameter("analyst.compress-file.filename")
    output = interface.Parameter("analyst.compress-file.output")

    def analyse(self, execution, sample):
        """
        Compress a file.
        """
        target = self.output.format(execution=execution)
        logger.info("Compressing '%s' to '%s'", self.filename, target)
        compress(self.filename, target)
    
    def discard(self, execution):
        """
        Discard the compressed file.
        """
        target = self.output.format(execution=execution)
        try:
            os.unlink(target)
        except OSError:
            # The file does not exist, this error is expected and can be
            # safely ignored.
            pass

# Register the analyst implementations.
interface.analysts.register("compress-slot", CompressSlotAnalyst)
interface.analysts.register("compress-file", CompressFileAnalyst)

