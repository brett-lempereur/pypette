"""
Memory image semantic feature digital forensic analyst.
"""

import bz2
import csv
import logging
import os
import re
import shutil
import subprocess

import pypette.interface as interface

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.analyst.volatile.semantic")

# The mapping of memory analysis module definitions.
definitions = {
    "connections": (
        "connscan",
        ["offset", "local", "remote", "pid"],
        r"(?P<offset>0x[0-9a-f]+) (?P<local>\d+\.\d+\.\d+\.\d+:\d+) +"
        r"(?P<remote>\d+\.\d+\.\d+\.\d+:\d+) +(?P<pid>\d+)"
    ),
    "handles": (
        "handles",
        ["offset", "pid", "handle", "access", "type", "details"],
        r"(?P<offset>0x[0-9a-f]+) +(?P<pid>\d+) +(?P<handle>0x[0-9a-f]+) +"
        r"(?P<access>0x[0-9a-f]+) (?P<type>[A-Z][a-z]+) +(?P<details>.*)"
    ),
    "processes": (
        "psscan",
        ["offset", "name", "pid", "ppid", "pdb", "created", "exited"],
        r"(?P<offset>0x[0-9a-f]+) (?P<name>.+?) +(?P<pid>\d+) +(?P<ppid>\d+) +"
        r"(?P<pdb>0x[0-9a-f]+) +(?P<created>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)? +"
        r"(?P<exited>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)?"
    ),
    "sockets": (
        "sockets",
        ["offset", "pid", "port", "proto", "protocol", "address", "created"],
        r"(?P<offset>0x[0-9a-f]+) +(?P<pid>\d+) +(?P<port>\d+) +(?P<proto>\d+) (?P<protocol>.+?) "
        r"+(?P<address>\d+\.\d+\.\d+\.\d+) +(?P<created>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)"
    ),
    "services": (
        "svcscan",
        ["offset", "order", "pid", "name", "display", "type", "state", "binary"],
        r"Offset: (?P<offset>.*)\nOrder: (?P<order>.*)\nProcess ID: (?P<pid>.*)\nService Name: "
        r"(?P<name>.*)\nDisplay Name: (?P<display>.*)\nService Type: (?P<type>.*)\nService State: "
        r"(?P<state>.*)\nBinary Path: (?P<binary>.*)"
    ),
    "modules": (
        "modules",
        ["offset", "name", "base", "size", "file"],
        r"(?P<offset>0x[0-9a-f]+) (?P<name>.+?) +(?P<base>0x[0-9a-f]+) +"
        r"(?P<size>0x[0-9a-f]+) +(?P<file>.+)"
    )
}

class MemoryFeatureAnalyst(interface.Analyst):
    """
    Memory image semantic feature analyst.

    Parameters:
    analyst.memory-feature.image -- the name of the memory image.
    analyst.memory-feature.profile -- the name of the memory image profile.
    analyst.memory-feature.modules -- the list of memory analysis modules.
    analyst.memory-feature.volatility -- the location of the volatility script.
    analyst.memory-feature.output -- the name of the output path.
    """

    # Memory image analysis parameters.
    image = interface.Parameter("analyst.memory-feature.image")
    profile = interface.Parameter("analyst.memory-feature.profile")
    modules = interface.Parameter("analyst.memory-feature.modules")
    volatility = interface.Parameter("analyst.memory-feature.volatility")

    # Output parameters.
    output = interface.Parameter("analyst.memory-feature.output")

    def analyse(self, execution, sample):
        """
        Analyse semantic features in a memory image.
        """
        path = self.output.format(execution=execution)
        os.mkdir(path)
        logger.info("Analysing semantic features from '%s'", self.image)
        for module in self.modules:
            command, headers, pattern = definitions[module]
            table = self.extract(sample[self.image], command, pattern)
            target = os.path.join(path, "{}.csv.bz2".format(module))
            self.write(target, headers, table)
        logger.info("Finished analysing semantic features")

    def extract(self, source, command, pattern):
        """
        Extract a table of semantic features from a memory image.

        Arguments:
        source -- the name of the memory image.
        command -- the name of the memory image analysis command.
        pattern -- the analysis command output pattern.
        """
        invocation = [
            self.volatility,
            "--profile",
            self.profile,
            "-f",
            source,
            command
        ]
        matcher = re.compile(pattern)
        try:
            data = subprocess.check_output(invocation)
            return [m.groupdict() for m in matcher.finditer(data)]
        except subprocess.CalledProcessError:
            logger.exception("Invocation of memory analysis command failed")
            raise

    def write(self, target, headers, table):
        """
        Write a table of extracted semantic features to a file.

        Arguments:
        target -- the name of the target file.
        headers -- the headers of the semantic feature table.
        table -- the semantic feature table.
        """
        handle = bz2.BZ2File(target, "wb")
        writer = csv.DictWriter(handle, headers)
        writer.writeheader()
        writer.writerows(table)
        handle.close()
    
    def discard(self, execution):
        """
        Discard the tables of semantic features.
        """
        path = self.output.format(execution=execution)
        try:
            shutil.rmtree(path)
        except OSError:
            # The file does not exist, this error is expected and can be
            # safely ignored.
            pass

# Register the analyst implementation.
interface.analysts.register("memory-feature", MemoryFeatureAnalyst)
