class Node:
    """A class representing the node baseclass"""
    def __init__(self, name, inputs, outputs):
        """Expects a iterable type with strings of inputs and a
        iterable type with strings symbolizing the outputs.
        """
        self._name = name
        self._inputs = inputs
        self._outputs = outputs
        self._incoming_edges = {} # All the outgoing edges key = number of input

    def execute(self):
        pass

    def add_edge(self, i, target):
        """Add a incoming edge. Adds a key value pair to the _incoming_edges
        list. Where the key i corresponds to the number of the input and the
        label target is the node object that is incoming.
        """
        self._incoming_edges[i] = target
