"""
Experiment metadata collection digital forensic analysts.
"""

import logging
import os

import yaml

import pypette.interface as interface

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.analyst.metadata")

class SampleMetadataAnalyst(interface.Analyst):
    """
    Sample metadata digital forensic analyst.
    
    Parameters:
    analyst.sample-metadata.slots -- the list of sample slots to record.
    analyst.sample-metadata.output -- the name of the output file.
    """
    
    # Metadata analysis parameters.
    slots = interface.Parameter("analyst.sample-metadata.slots")
    output = interface.Parameter("analyst.sample-metadata.output")
    
    def analyse(self, execution, sample):
        """
        Collect metadata from a sample.
        """
        logger.info("Collecting metadata for execution '%s'", execution)
        # Encode the sample metadata in a document.
        document = yaml.dump({slot: sample[slot] for slot in self.slots})
        # Save the metadata document to a file.
        output_filename = self.output.format(execution=execution)
        with open(output_filename, "w") as handle:
            handle.write(document)
    
    def discard(self, execution):
        """
        Discard the collected metadata.
        """
        output_filename = self.output.format(execution=execution)
        try:
            os.unlink(output_filename)
        except OSError:
            # The file does not exist, this error is expected and can be
            # safely ignored.
            pass

class ExperimentMetadataAnalyst(interface.Analyst):
    """
    Experiment metadata digital forensic analyst.
    """
    
    # Metadata analysis parameters.
    slots = interface.Parameter("analyst.experiment-metadata.slots")
    output = interface.Parameter("analyst.experiment-metadata.output")
    
    def __init__(self, parameters):
        """
        Initialise a new experiment metadata analyst.
        """
        super(ExperimentMetadataAnalyst, self).__init__(parameters)
        self.table = {}
    
    def analyse(self, execution, sample):
        """
        Collect metadata from a sample.
        """
        self.table[execution] = sample
    
    def collate(self):
        """
        Collate metadata from an experiment.
        """
        logger.info("Collating metadata for experiment")
        document = yaml.dump(self.table)
        with open(self.output, "w") as handle:
            handle.write(document)
    
    def discard(self, execution):
        """
        Discard the collected metadata.
        """
        try:
            del self.table[execution]
        except KeyError:
            # The record does not exist, this error is expected and can be
            # safely ignored.
            pass

# Register the analyst implementations.
interface.analysts.register("sample-metadata", SampleMetadataAnalyst)
interface.analysts.register("experiment-metadata", ExperimentMetadataAnalyst)

