"""
Attach virtual machine disk images and their partitions to the host.
"""

import glob
import logging
import os
import re
import subprocess
import tempfile
import time

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.volume")

def attach(filename):
    """
    Attach a compressed disk image to the host and return the path
    of the device node.

    Arguments:
    filename -- the location of the disk image.
    """
    # Determine the actual filename of the image.
    source = os.path.realpath(filename)
    # Select the first available device node.
    device = available_device_node()
    target = os.path.join("/dev", device)
    # Attach the network block device to the host.
    logger.info("Attaching drive '%s' to device '%s'", source, target)
    subprocess.check_call(["qemu-nbd", "-n", "-c", target, source])
    # Return the path to the caller.
    return target

def detach(device):
    """
    Detach a virtual disk image from the host.

    Arguments:
    device -- the device node at which the image is attached.
    """
    logger.info("Detaching device '%s'")
    subprocess.check_call(["qemu-nbd", "-d", device])

def mount(device):
    """
    Attach a volume to the host filesystem.

    Arguments:
    device -- the device node at which the volume is attached.
    """
    path = tempfile.mkdtemp(".mount")
    logger.info("Mounting '%s' at '%s'", device, path)
    subprocess.check_call(["mount", "-o", "ro,force", device, path])
    return path

def unmount(path):
    """
    Detach a volume from the host filesystem.

    Arguments:
    path -- the location at which the volume is mounted.
    """
    logger.info("Unmounting '%s'", path)
    subprocess.check_call(["umount", path])
    os.rmdir(path)

def partition(device, number):
    """
    Return the device node of a volume partition.

    Arguments:
    device -- the device node at which the volume is attached.
    number -- the number of the volume partition.
    """
    return "{}p{}".format(device, number)

def wait_for_partition(device):
    """
    Wait for a partition device to become available.

    Arguments:
    device -- the device node at which the volume is attached.
    """
    logger.info("Waiting for partition '%s' to become available", device)
    node = os.path.basename(device)
    while not node in attached_partitions():
        time.sleep(0.1)

def device_nodes():
    """
    Return the set of network block device nodes.
    """
    return set([os.path.basename(d) for d in glob.glob("/dev/nbd?")])

def attached_device_nodes():
    """
    Return the set of attached network block device nodes.
    """
    return set(re.findall("nbd[0-9]", open("/proc/partitions", "r").read()))

def available_device_node():
    """
    Return the next available network block device node.
    """
    available = device_nodes().difference(attached_device_nodes())
    return available.pop()

def attached_partitions():
    """
    Return the set of attached network block device partition nodes.
    """
    table = open("/proc/partitions", "r").read()
    return set(re.findall("nbd[0-9]p[0-9]", table))
