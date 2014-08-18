"""
Memory image and memory page digital forensic analysts.
"""

import bz2
import csv
import hashlib
import logging
import os
import re
import subprocess

import pypette.interface as interface

# Memory page analysis constants.
PAGE_COMMAND = "checksum"
PAGE_HEADERS = ["offset", "size", "checksum"]
PAGE_PATTERN = r"(?P<offset>0x[0-9a-f]+) (?P<size>0x[0-9a-f]+) (?P<checksum>.+)"

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.analyst.volatile.structural")

class PhysicalPageAnalyst(interface.Analyst):
    """
    Physical memory page digital forensic analyst.

    Parameters:
    analyst.physical-page.image -- the name of the memory image file.
    analyst.physical-page.page-size -- the page size of the memory image.
    analyst.physical-page.output -- the name of the output file.
    """

    # Memory image analysis parameters.
    image = interface.Parameter("analyst.physical-page.image")
    page_size = interface.Parameter("analyst.physical-page.page-size")

    # Output parameters.
    output = interface.Parameter("analyst.physical-page.output")

    def analyse(self, execution, sample):
        """
        Analyse a memory image.
        """
        import pypette.analyst.storage as storage
        logger.info("Generating a hash of physical pages in '%s'", self.image)
        output_filename = self.output.format(execution=execution)
        handle = bz2.BZ2File(output_filename, "w")
        for block in storage.blocks(sample[self.image], self.page_size):
            checksum = hashlib.md5(block)
            handle.write(checksum.hexdigest())
            handle.write("\n")
        logger.info("Finished physical memory page analysis")
        handle.close()
    
    def discard(self, execution):
        """
        Discard the memory image physical page hash database.
        """
        output_filename = self.output.format(execution=execution)
        try:
            os.unlink(output_filename)
        except OSError:
            # The file does not exist, this error is expected and can be
            # safely ignored.
            pass

class LogicalPageAnalyst(interface.Analyst):
    """
    Logical memory page digital forensic analyst.

    Parameters:
    analyst.logical-page.image -- the name of the memory image file.
    analyst.logical-page.volatility -- the location of the volatility script.
    analyst.logical-page.output -- the name of the output file.
    """

    # Memory image analysis parameters.
    image = interface.Parameter("analyst.logical-page.image")
    volatility = interface.Parameter("analyst.logical-page.volatility")

    # Output parameters.
    output = interface.Parameter("analyst.logical-page.output")

    def analyse(self, execution, sample):
        """
        Analyse pages in a memory image.
        """
        logger.info("Generating a hash of logical pages in '%s'", self.image)
        # Create a file to contain the memory page analysis results.
        output_filename = self.output.format(execution=execution)
        handle = bz2.BZ2File(output_filename, "wb")
        writer = csv.DictWriter(handle, PAGE_HEADERS)
        writer.writeheader()
        # Invoke the memory image analysis process.
        invocation = [self.volatility, "-f", sample[self.image], PAGE_COMMAND]
        process = subprocess.Popen(invocation, stdout=subprocess.PIPE)
        # Extract the information describing each page in the memory image.
        pattern = re.compile(PAGE_PATTERN)
        for line in process.stdout:
            match = pattern.match(line)
            if not match is None:
                writer.writerow(match.groupdict())
        # Close the output handle and wait for the analysis process.
        logger.info("Finished logical memory page analysis")
        handle.close()
        process.wait()
    
    def discard(self, execution):
        """
        Discard the memory image logical page hash database.
        """
        output_filename = self.output.format(execution=execution)
        try:
            os.unlink(output_filename)
        except OSError:
            # The file does not exist, this error is expected and can be
            # safely ignored.
            pass

# Register the analyst implementations.
interface.analysts.register("physical-page", PhysicalPageAnalyst)
interface.analysts.register("logical-page", LogicalPageAnalyst)

