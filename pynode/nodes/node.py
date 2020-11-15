class Node:
    """A class representing the node baseclass"""
    def __init__(self, name, inputs, outputs):
        """Expects a iterable type with strings of inputs and a
        iterable type with strings symbolizing the outputs.
        """
        self._name = name
        self._inputs = inputs
        self._outputs = outputs

    def execute(self):
        pass
