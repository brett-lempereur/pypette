"""
Live digital forensic component interface and registry.
"""

class Parameter(object):
    """
    Live digital forensic experiment parameter.

    Attributes:
    name -- the name of the parameter.
    """
    
    def __init__(self, name):
        """
        Initialise a new parameter.
        """
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.parameters[self.name]

    def __set__(self, instance, value):
        raise AttributeError("Parameter dictionary is read-only")

class Slot(object):
    """
    Live digital forensic experiment sample output slot.

    Attributes:
    name -- the name of the output slot.
    """
    
    def __init__(self, name):
        """
        Initialise a new sample output slot.
        """
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.output[self.name]

    def __set__(self, instance, value):
        instance.output[self.name] = value

class Analyst(object):
    """
    Live digital forensic experiment analyst.

    Attributes:
    parameters -- the analyst parameter dictionary.
    """
    
    def __init__(self, parameters):
        """
        Initialise a new live digital forensic analyst.

        Arguments:
        parameters -- the analyst parameter dictionary.
        """
        self.parameters = parameters

    def analyse(self, execution, sample):
        """
        Analyse an execution of a live digital forensic experiment.

        Arguments:
        execution -- the unique experiment execution identifier.
        sample -- the sample collected by the technique.
        """
        raise NotImplementedError()

    def collate(self):
        """
        Collate the results of analysis.
        """
        pass
    
    def discard(self, execution):
        """
        Discard the results of analysing an execution of a live digital
        forensic experiment.
        
        Arguments:
        execution -- the unique experiment execution identifier.
        """
        pass

class Technique(object):
    """
    Live digital forensic experiment technique.

    Attributes:
    parameters -- the technique parameter dictionary.
    output -- the sample output dictionary.
    """

    def __init__(self, parameters):
        """
        Initialise a new live digital forensic technique.

        Arguments:
        parameters -- the technique parameter dictionary.
        """
        self.parameters = parameters
        self.output = {}
    
    def allocate(self):
        """
        Allocate temporary resources.
        """
        pass

    def sample(self):
        """
        Sample an execution of a live digital forensic experiment.
        """
        raise NotImplementedError()

    def release(self):
        """
        Release temporary resources.
        """
        pass

class Behaviour(object):
    """
    Live digital forensic experimental behaviour.
    """
    
    def allocate_behaviour(self):
        """
        Allocate temporary resources.
        """
        pass
    
    def release_behaviour(self):
        """
        Release temporary resources.
        """
        pass

class Registry(object):
    """
    Live digital forensic experiment component registry.

    Attributes:
    components -- the dictionary of registered components.
    """

    def __init__(self):
        """
        Initialise a new component registry.
        """
        self.components = {}
    
    def register(self, name, component):
        """
        Register a component implementation.

        Arguments:
        name -- the name of the component.
        component -- the component implementation.
        """
        self.components[name] = component

    def get(self, name):
        """
        Return a component implementation.

        Arguments:
        name -- the name of the components.
        """
        return self.components[name]

# Create the global analyst and technique registries.
analysts = Registry()
techniques = Registry()

