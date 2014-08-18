"""
This module provides support for hosting and interacting with virtual
machines.
"""

import json
import logging

import libvirt
import libvirt_qemu

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.emulator")

class Emulator(object):
    """
    Virtual machine emulator.

    Attributes:
    connection -- the connection to the virtualisation platform.
    domain -- the virtual machine domain.
    """

    def __init__(self, address, name):
        """
        Initialise a new virtual machine emulator.

        Arguments:
        address -- the address of the virtualisation platform.
        name -- the name of the virtual machine domain.
        """
        self.connection = libvirt.open(address)
        self.domain = self.connection.lookupByName(name)

    def create(self):
        """
        Create the virtual machine.
        """
        self.domain.createWithFlags(libvirt.VIR_DOMAIN_START_PAUSED)

    def revert(self, name):
        """
        Revert the virtual machine to a snapshot.

        Arguments:
        name -- the name of the virtual machine snapshot.
        """
        snapshot = self.domain.snapshotLookupByName(name, 0)
        flag = libvirt.VIR_DOMAIN_SNAPSHOT_REVERT_PAUSED
        self.domain.revertToSnapshot(snapshot, flag)

    def resume(self):
        """
        Resume execution of the virtual machine.
        """
        self.domain.resume()

    def suspend(self):
        """
        Suspend execution of the virtual machine.
        """
        self.domain.suspend()

    def save_memory(self, filename):
        """
        Save an image of virtual machine memory to a file.

        Arguments:
        filename -- the location of the memory image.
        """
        self._native_command("pmemsave", val=0, size=self.memory,
                             filename=filename)

    def change_optical(self, device, filename):
        """
        Change the media in an optical device.

        Arguments:
        device -- the name of the optical device.
        filename -- the location of the optical media image.
        """
        statement = """
        <disk type='file' device='cdrom'>
            <source file='{}'/>
            <target dev='{}'/>
            <readonly/>
         </disk>
        """.format(filename, device)
        self.domain.updateDeviceFlags(statement, libvirt.VIR_DOMAIN_AFFECT_LIVE)

    def eject_optical(self, device):
        """
        Eject the media from an optical device.

        Arguments:
        device -- the name of the optical device.
        """
        statement = """
        <disk type='file' device='cdrom'>
            <target dev='{}'/>
            <readonly/>
         </disk>
        """.format(device)
        self.domain.updateDeviceFlags(statement, libvirt.VIR_DOMAIN_AFFECT_LIVE)

    def attach_host_usb(self, vendor, product):
        """
        Attach a host USB device.

        Arguments:
        vendor -- the vendor identity of the device.
        product -- the product identity of the device.
        """
        statement = """
        <hostdev mode='subsystem' type='usb'>
            <source>
                <vendor id='{}'/>
                <product id='{}'/>
            </source>
        </hostdev>
        """.format(vendor, product)
        self.domain.attachDeviceFlags(statement, libvirt.VIR_DOMAIN_AFFECT_LIVE)

    def detach_host_usb(self, vendor, product):
        """
        Detach a host USB device.

        Arguments:
        vendor -- the vendor identity of the device.
        product -- the product identity of the device.
        """
        statement = """
        <hostdev mode='subsystem' type='usb'>
            <source>
                <vendor id='{}'/>
                <product id='{}'/>
            </source>
        </hostdev>
        """.format(vendor, product)
        self.domain.detachDeviceFlags(statement, libvirt.VIR_DOMAIN_AFFECT_LIVE)

    @property
    def memory(self):
        """
        The amount of memory allocated to the virtual machine, in bytes.
        """
        return self.domain.memoryStats()["actual"] * 1024

    def _native_command(self, command, **kwargs):
        """
        Invoke a command directly on the virtual machine manager.

        This method is unsafe, in that it allows a developer to bypass
        the integrity checks of the virtualisation platform.  It should
        be used sparingly, and only where there is no alternative.

        Arguments:
        command -- the name of the command to invoke.
        """
        message = json.dumps({"execute": command, "arguments": kwargs})
        data = libvirt_qemu.qemuMonitorCommand(self.domain, message, 0)
        try:
            response = json.loads(data)
            if "return" in response:
                return response["return"]
            else:
                logger.critical("Unknown response from console: %s", response)
                raise RuntimeError("Unknown response from console")
        except TypeError:
            raise RuntimeError("Malformed message from virtual machine")

    def close(self):
        """
        Close the virtual machine emulator.
        """
        self.domain.destroy()

