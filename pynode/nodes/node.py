class Node:
    """A class representing the node baseclass"""
    def __init__(self, inputs, outputs):
        """Expects a iterable type with strings of inputs and a
        iterable type with strings symbolizing the outputs.
        """
        self._inputs = inputs
        self._inputs = outputs

    def execute(self):
        pass
