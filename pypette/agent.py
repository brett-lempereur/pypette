"""
This module provides a communication mechanism for interacting with the
virtual machine guest agent.
"""

import json
import logging
import socket

# Agent command timeout constants.
EXECUTE_TIMEOUT = None
MONITOR_TIMEOUT = None
FIND_TIMEOUT = 30
EJECT_TIMEOUT = 30
FLUSH_TIMEOUT = 30
STATUS_TIMEOUT = 30

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.agent")

class Agent(object):
    """
    Live digital forensic guest agent.

    Attributes:
    console -- the guest agent console.
    """

    def __init__(self, address):
        """
        Initialise a new live digital forensic guest agent.

        Arguments:
        address -- the address of the guest agent server.
        """
        self.console = Console(address)
        self.console.connect()

    def execute(self, command, shell=False, cwd=None):
        """
        Execute a process within the guest operating system.

        Arguments:
        command -- the command-line invocation.
        shell -- invoke the command in a shell (default False).
        cwd -- the working directory for the invocation (default None).
        """
        return self.console.call("execute", {
            "command": command,
            "shell": shell,
            "cwd": cwd
        }, timeout=EXECUTE_TIMEOUT)

    def monitor(self, command, interval=5, cwd=None):
        """
        Monitor the execution of a process within the guest environment.

        Arguments:
        command -- the command-line invocation of the process.
        interval -- the sampling interval (default 1).
        cwd -- the working directory of the process (default None).
        """
        return self.console.call("monitor", {
            "command": command,
            "interval": interval,
            "cwd": cwd
        }, timeout=MONITOR_TIMEOUT)

    def find(self, tag):
        """
        Find removable media within the guest operating system.

        Arguments:
        tag -- the identity of the volume to find.
        """
        return self.console.call("find", {
            "tag": tag
        }, timeout=FIND_TIMEOUT)

    def eject(self, tag):
        """
        Eject removable media from the guest operating system.

        Arguments:
        tag -- the identity of the volume to eject.
        """
        return self.console.call("eject", {
            "tag": tag
        }, timeout=EJECT_TIMEOUT)

    def flush(self, tag):
        """
        Flush the contents of a volume buffer in the guest operating
        system.

        Argument:
        tag -- the identity of the volume to flush.
        """
        return self.console.call("flush", {
            "tag": tag
        }, timeout=FLUSH_TIMEOUT)

    def status(self):
        """
        Sample the performance status of the live digital forensic guest
        agent.
        """
        return self.console.call("status", {}, timeout=STATUS_TIMEOUT)

class Console(object):
    """
    Guest agent console.

    Attributes:
    address -- the address of the guest agent server.
    """

    CONNECT_TIMEOUT = 5
    REQUEST_TIMEOUT = 5

    def __init__(self, address):
        """
        Initialise a new guest agent console.

        Arguments:
        address -- the address of the guest agent server.
        """
        self.address = address
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.buffer = ""

    def connect(self):
        """
        Open the connection to the guest agent.
        """
        try:
            self.socket.settimeout(self.CONNECT_TIMEOUT)
            self.socket.connect(self.address)
        finally:
            self.socket.settimeout(None)

    def call(self, command, parameters, timeout=None):
        """
        Call a command on the guest agent and return the result.

        Arguments:
        command -- the name of the requested command.
        parameters -- the parameters of the requested command.
        timeout -- the duration to wait for a reply (default None).
        """
        self.request(command, parameters)
        result = self.receive(timeout=timeout)
        if isinstance(result, Reply):
            return result.parameters
        if isinstance(result, Error):
            raise RuntimeError("Guest agent error in {}: {}".format(
                               result.source, result.message))
        raise RuntimeError("Guest agent call returned unexpected type")

    def request(self, command, parameters):
        """
        Send a request to the guest agent.

        Arguments:
        command -- the name of the requested command.
        parameters -- the parameters of the requested command.
        """
        message = json.dumps({
            "request": {
                "command": command,
                "parameters": parameters
            }
        })
        try:
            self.socket.settimeout(self.REQUEST_TIMEOUT)
            self.socket.sendall(message)
            self.socket.sendall("\n")
        finally:
            self.socket.settimeout(None)

    def receive(self, timeout=None):
        """
        Receive a response from the guest agent.
        
        Arguments:
        timeout -- the duration to wait for a reply (default None).
        """
        try:
            # Receive at least one line of text from the guest agent.
            self.socket.settimeout(timeout)
            while not "\n" in self.buffer:
                self.buffer += self.socket.recv(1024)
            line, self.buffer = self.buffer.split("\n", 1)
            # Interpret the received line as a protocol message.
            message = json.loads(line)
            if "reply" in message:
                command = message["reply"]["command"]
                parameters = message["reply"]["parameters"]
                return Reply(command, parameters)
            if "error" in message:
                source = message["error"]["source"]
                description = message["error"]["message"]
                return Error(source, description)
            raise RuntimeError("Console received unexpected message")
        except TypeError:
            raise RuntimeError("Console received malformed message")
        except ValueError:
            raise RuntimeError("Console received malformed message")
        except KeyError:
            raise RuntimeError("Console received malformed message")
        finally:
            self.socket.settimeout(None)

    def close(self):
        """
        Close the connection to the guest agent.
        """
        self.socket.close()

class Reply(object):
    """
    Guest agent reply.

    Attributes:
    command -- the source of the reply.
    parameters -- the parameters of the reply.
    """

    def __init__(self, command, parameters):
        """
        Initialise a new guest agent reply.

        Arguments:
        command -- the source of the reply.
        parameters -- the parameters of the reply.
        """
        self.command = command
        self.parameters = parameters

class Error(object):
    """
    Guest agent error.

    Attributes:
    source -- the source of the error.
    message -- the error message.
    """

    def __init__(self, source, message):
        """
        Initialise a new guest agent error.

        Arguments:
        source -- the source of the error.
        message -- the error message.
        """
        self.source = source
        self.message = message
