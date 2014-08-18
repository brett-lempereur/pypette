"""
Live digital forensic experiment definition and control.
"""

import logging
import uuid

import yaml

import pypette.interface as interface

# Create the module-wide logger instance.
logger = logging.getLogger("pypette.experiment")

def conduct(definition):
    """
    Conduct a live digital forensic experiment.

    Arguments:
    definition -- the experiment definition.
    """
    identities = [uuid.uuid4() for i in range(definition.executions)]
    analysts = get_analysts(definition)
    for execution in identities:
        technique = get_technique(definition)
        try:
            technique.allocate()
            technique.sample()
            for analyst in analysts:
                analyst.analyse(execution, technique.output)
        except:
            logger.exception("Exception during experiment execution")
            for analyst in analysts:
                analyst.discard(execution)
            identities.append(uuid.uuid4())
        finally:
            technique.release()
    for analyst in analysts:
        analyst.collate()

def get_analysts(definition):
    """
    Return a list of instances of the live digital forensic analysts
    specified in an experiment definition.

    Arguments:
    definition -- the experiment definition.
    """
    container = []
    for analyst in definition.analysts:
        component = interface.analysts.get(analyst.name)
        instance = component(analyst.parameters)
        container.append(instance)
    return container

def get_technique(definition):
    """
    Return an instance of the live digital forensic technique specified
    in an experiment definition.

    Arguments:
    definition -- the experiment definition.
    """
    component = interface.techniques.get(definition.technique.name)
    instance = component(definition.technique.parameters)
    return instance

class Definition(object):
    """
    Live digital forensic experiment definition.
    """

    def __init__(self, document):
        """
        Initialise a new experiment definition.

        Arguments:
        document -- the experiment definition document.
        """
        self.tree = yaml.load(document)
    
    @property
    def name(self):
        """
        The name of the experiment.
        """
        return self.tree["name"]

    @property
    def executions(self):
        """
        The number of executions of the experiment.
        """
        return self.tree["executions"]

    @property
    def parameters(self):
        """
        The parameters of the experiment.
        """
        return self.tree["parameters"]

    @property
    def technique(self):
        """
        The live digital forensic technique.
        """
        name = self.tree["technique"]["name"]
        parameters = self.tree["technique"]["parameters"]
        return ComponentDefinition(name, parameters)

    @property
    def analysts(self):
        """
        The live digital forensic analysts.
        """
        container = []
        for analyst in self.tree["analysts"]:
            name = analyst["name"]
            parameters = analyst["parameters"]
            container.append(ComponentDefinition(name, parameters))
        return container

class ComponentDefinition(object):
    """
    Live digital forensic experiment component definition.

    Attributes:
    name -- the name of the component.
    parameters -- the parameters of the component.
    """
    
    def __init__(self, name, parameters):
        """
        Initialise a new component definition.

        Arguments:
        name -- the name of the component.
        parameters -- the parameters of the component.
        """
        self.name = name
        self.parameters = parameters

