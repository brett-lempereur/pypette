"""
Live digital forensic evidence vector behaviours.
"""

import logging
import os
import shutil
import tempfile

import pypette.interface as interface
import pypette.volume as volume

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.technique.behaviour.toolkit")

class FixedDriveAcquisitionVector(interface.Behaviour):
    """
    Fixed local drive live digital forensic acquisition vector
    behaviour.

    Parameters:
    technique.vector.filename -- the name of the disk image file.
    technique.vector.partition -- the index of the partition.
    technique.vector.tag -- the identification tag of the vector.
    technique.vector.image -- the filename of the memory image on the vector.
    
    Slots:
    memory.acquired -- the memory image acquired by the toolkit.
    """

    # Fixed drive acquisition vector parameters.
    vector_filename = interface.Parameter("technique.vector.filename")
    vector_partition = interface.Parameter("technique.vector.partition")
    vector_tag = interface.Parameter("technique.vector.tag")
    vector_image = interface.Parameter("technique.vector.image")
    
    # Memory image slots.
    image_acquired = interface.Slot("memory.acquired")
    
    def allocate_behaviour(self):
        """
        Allocate temporary resources.
        """
        super(FixedDriveAcquisitionVector, self).allocate_behaviour()
        logger.info("Allocating resources")
        self.image_acquired = tempfile.mktemp(".memory")

    def attach_vector(self, domain, agent):
        """
        Attach the fixed local drive acquisition vector to the domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        logger.info("Verifying that the fixed drive is attached to the domain")
        agent.find(self.vector_tag)

    def detach_vector(self, domain, agent):
        """
        Detach the fixed local drive acquisition vector from the domain.

        Arguments:
        domain -- the virtual machine domain.
        agent -- the virtual machine guest agent.
        """
        logger.info("Flushing the cache from the fixed drive")
        agent.flush(self.vector_tag)

    def transfer_acquired_image(self):
        """
        Transfer the acquired memory image from the acquisition vector
        to the host machine.
        """
        # Attach the disk image and mount the partition on the host machine.
        logger.info("Attaching and mounting the acquisition vector")
        device = volume.attach(self.vector_filename)
        partition_device = volume.partition(device, self.vector_partition)
        volume.wait_for_partition(partition_device)
        path = volume.mount(partition_device)
        # Copy the memory image from the vector partition.
        logger.info("Copying the memory image from the acquisition vector")
        image_filename = os.path.join(path, self.vector_image)
        shutil.copy(image_filename, self.image_acquired)
        # Unmount the partition and detach the disk image.
        logger.info("Unmounting and detaching the acquisition vector")
        volume.unmount(path)
        volume.detach(device)
    
    def release_behaviour(self):
        """
        Release temporary resources.
        """
        super(FixedDriveAcquisitionVector, self).release_behaviour()
        logger.info("Releasing resources")
        if os.path.exists(self.image_acquired):
            os.unlink(self.image_acquired)

