"""
Block storage and file-system digital forensic analysts.
"""

import bz2
import csv
import hashlib
import logging
import os

import pypette.interface as interface
import pypette.volume as volume

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.analyst.storage")

def blocks(filename, block_size):
    """
    Return a generator that yields blocks from a file.

    Arguments:
    filename -- the name of the file.
    block_size -- the size of each block.
    """
    with open(filename, "rb") as handle:
        block = handle.read(block_size)
        while block:
            yield block
            block = handle.read(block_size)

def filenames(path):
    """
    Return a generator that yields all files in directory tree.

    Arguments:
    path -- the path of the directory tree.
    """
    for node, leaves, names in os.walk(path):
        for name in names:
            filename = os.path.join(node, name)
            if not os.path.islink(filename) and os.path.isfile(filename):
                yield filename

class BlockStorageAnalyst(interface.Analyst):
    """
    Block storage digital forensic analyst.

    Parameters:
    analyst.block-storage.image -- the name of the image file.
    analyst.block-storage.partition -- the index of the partition.
    analyst.block-storage.block-size -- the block size of the partition.
    analyst.block-storage.output -- the name of the output file.
    """

    # Block storage analysis parameters.
    image = interface.Parameter("analyst.block-storage.image")
    partition = interface.Parameter("analyst.block-storage.partition")
    block_size = interface.Parameter("analyst.block-storage.block-size")

    # Output parameters.
    output = interface.Parameter("analyst.block-storage.output")

    def analyse(self, execution, sample):
        """
        Analyse a block storage partition.
        """
        # Attach the disk image to the host machine.
        logger.info("Attaching '%s' for block-storage analysis", self.image)
        device = volume.attach(self.image)
        try:
            partition_device = volume.partition(device, self.partition)
            volume.wait_for_partition(partition_device)
            # Open the output handle.
            logger.info("Generating a hash of each block on the partition")
            output_filename = self.output.format(execution=execution)
            handle = bz2.BZ2File(output_filename, "w")
            # Generate a hash of each block in the partition.
            for block in blocks(partition_device, self.block_size):
                checksum = hashlib.md5(block)
                handle.write(checksum.hexdigest())
                handle.write("\n")
            # Close output handle and detach the disk image.
            logger.info("Finished block-storage analysis, detaching volume")
            handle.close()
        finally:
            volume.detach(device)
    
    def discard(self, execution):
        """
        Discard the block storage hash database.
        """
        output_filename = self.output.format(execution=execution)
        try:
            os.unlink(output_filename)
        except OSError:
            # The file does not exist, this error is expected and can be
            # safely ignored.
            pass

class FileSystemAnalyst(interface.Analyst):
    """
    File-system digital forensic analyst.

    Parameters:
    analyst.file-system.image -- the name of the image file.
    analyst.file-system.partition -- the index of the partition.
    analyst.file-system.output -- the name of the output file.
    """

    # File-system analysis parameters.
    image = interface.Parameter("analyst.file-system.image")
    partition = interface.Parameter("analyst.file-system.partition")

    # Output parameters.
    output = interface.Parameter("analyst.file-system.output")

    def analyse(self, execution, sample):
        """
        Analyse a file-system.
        """
        # Attach the disk image and mount the partition on the host machine.
        logger.info("Attaching '%s' for file-system analysis", self.image)
        device = volume.attach(self.image)
        try:
            partition_device = volume.partition(device, self.partition)
            volume.wait_for_partition(partition_device)
            path = volume.mount(partition_device)
            # Open the output handle.
            logger.info("Generating a hash of each file on the volume")
            output_filename = self.output.format(execution=execution)
            handle = bz2.BZ2File(output_filename, "wb")
            writer = csv.writer(handle)
            writer.writerow(["hash", "filename"])
            # Generate a hash of each file in the partition.
            for filename in filenames(path):
                checksum = hashlib.md5()
                for block in blocks(filename, 4096):
                    checksum.update(block)
                relative = os.path.relpath(filename, path)
                writer.writerow([checksum.hexdigest(), relative])
            # Close the output handle and detach the disk image.
            logger.info("Finished file-system analysis, detaching volume")
            handle.close()
            volume.unmount(path)
        finally:
            volume.detach(device)
    
    def discard(self, execution):
        """
        Discard the file-system hash database.
        """
        output_filename = self.output.format(execution=execution)
        try:
            os.unlink(output_filename)
        except OSError:
            # The file does not exist, this error is expected and can be
            # safely ignored.
            pass

# Register the analyst implementations.
interface.analysts.register("block-storage", BlockStorageAnalyst)
interface.analysts.register("file-system", FileSystemAnalyst)
