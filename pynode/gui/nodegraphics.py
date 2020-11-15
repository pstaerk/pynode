import pyglet
from pynode.gui.utils import distribute_in_length
from pynode.gui.utils import is_in_rectangle

LENGTH_INPUT = 10
LENGTH_OUTPUT = 10
MINIMUM_LENGTH = 100
MINIMUM_HEIGHT = 100
INPUTS_OFFSET = 1 # Offset of input rectangles from left side
INPUTS_UPPER_LOWER = 10 # Inputs are not allowed to be place this much from the border
OUTPUTS_OFFSET = 1 # Offset of input rectangles from left side
OUTPUTS_UPPER_LOWER = 10 # Inputs are not allowed to be place this much from the border
NODE_COLOR = (30,65,99)
INPUT_COLOR = (26,99,31)
OUTPUT_COLOR = (99,87,29)
LABEL_HEIGHT = 20
LABEL_COLOR = (75,72,99)
LABEL_YOFFSET = 4

class NodeGraphics:
    """A graphical representation of a node."""
    def __init__(self, node, position, mainbatch, nodebatch, labelbatch):
        """Create a node pyglet object to be displayed on the graphical ui.
        """
        self._node = node # keep track of the node object
        self._x, self._y = position[0], position[1]
        self._shapes = []
        self._lines = [] # lines which are connected, stores tuples of type and line object
        self._inputs = [] # input graphical representations
        self._outputs = [] # output graphical representations
        self._mainbatch = mainbatch # batch context to draw shapes efficiently
        self._nodebatch = nodebatch 
        self._labelbatch = labelbatch
        self._create_shapes()

    def _calc_shapes(self):
        """Calculate the relevant dimensions of the box from the number of inputs,
        label etc.
        """
        self._width = MINIMUM_LENGTH + len(self._node._name[10:])*10
        self._height = MINIMUM_HEIGHT
        if len(self._node._inputs) > 3: # Make rect higher if more than 3 inputs
            self._height += len(self._node._inputs[4:])*5

    def _create_shapes(self):
        """Create the necessary pyglet shapes to display.
        """
        self._calc_shapes() # calculate the needed width and height etc
        self._create_basic_shape()
        self._create_inputs_dockers()
        self._create_outputs_dockers()

    def _create_basic_shape(self):
        """Create the basic shape that is the node.
        """
        rect = pyglet.shapes.Rectangle(self._x, self._y, self._width, self._height,
                color=NODE_COLOR, batch=self._mainbatch, group=self._nodebatch)
        # Add a label bar above the rectangle
        rect2 = pyglet.shapes.Rectangle(self._x, self._y+self._height, self._width, 
                LABEL_HEIGHT, color=LABEL_COLOR, batch=self._mainbatch, group=self._nodebatch)
        lab = pyglet.text.Label(text=self._node._name, x=self._x, 
                y=self._y+self._height+LABEL_YOFFSET, batch=self._mainbatch, group=self._labelbatch)
        self._shapes.append(rect)
        self._shapes.append(rect2)
        self._shapes.append(lab)

    def _create_outputs_dockers(self):
        """Create the docking symbols for the outputs.
        """
        nr_ins = len(self._node._outputs)
        for i, inp in enumerate(self._node._outputs):
            # Calculate the positions of the inputs
            place_height = self._height - 2*OUTPUTS_UPPER_LOWER # Length onto which ins placed
            vpos = distribute_in_length(i, nr_ins, LENGTH_OUTPUT, place_height)
            vpos += self._y + OUTPUTS_UPPER_LOWER
            hpos = self._x - OUTPUTS_OFFSET + self._width - LENGTH_OUTPUT
            trect = pyglet.shapes.Rectangle(hpos, vpos, LENGTH_OUTPUT, LENGTH_OUTPUT,
                    color=OUTPUT_COLOR, batch=self._mainbatch, group=self._nodebatch)
            self._shapes.append(trect)

            # Place labels
            labx, laby = hpos, vpos, 
            tlab = pyglet.text.Label(inp, x=labx, y=laby, anchor_x='right', align='right', 
                    batch=self._mainbatch, group=self._labelbatch)
            self._shapes.append(tlab)
            self._outputs.append(trect)

    def _create_inputs_dockers(self):
        """Create the docking symbols for the inputs.
        """
        nr_ins = len(self._node._inputs)
        for i, inp in enumerate(self._node._inputs):
            # Calculate the positions of the inputs
            place_height = self._height - 2*INPUTS_UPPER_LOWER # Length onto which ins placed
            vpos = distribute_in_length(i, nr_ins, LENGTH_INPUT, place_height)
            vpos += self._y + INPUTS_UPPER_LOWER
            hpos = self._x + INPUTS_OFFSET
            trect = pyglet.shapes.Rectangle(hpos, vpos, LENGTH_INPUT, LENGTH_INPUT,
                    color=INPUT_COLOR, batch=self._mainbatch, group=self._nodebatch)
            self._shapes.append(trect)

            # Place labels
            labx, laby = hpos + LENGTH_INPUT, vpos, 
            tlab = pyglet.text.Label(inp, x=labx, y=laby, batch=self._mainbatch, group=self._labelbatch)
            self._shapes.append(tlab)
            self._inputs.append(trect)

    def add_line(self, line_obj, type_of_line):
        """Add a line, which is connected to the node and needs to be updated
        if the object were to move. type_of_line has to specify if this is the
        starting point or the end point, i.e. 'end'/'start'
        """
        self._lines = [(line_obj, type_of_line)]

    def check_click_location(self, x, y):
        """Check if x, y coordinates are near a input or output.
        :returns: tuple with 'in'/'out', rectangle object and the number of the input/output
        that is clicked
        """
        # check inputs
        for j, i in enumerate(self._inputs):
            if is_in_rectangle(x, y, i):
                return 'in', i, j

        # check outputs
        for i in self._outputs:
            if is_in_rectangle(x, y, i):
                return 'out', i, j

        return '', False, -1

    def move(self, rel_x, rel_y):
        """Move the object by the relative amount rel_x, rel_y.
        """
        for s in self._shapes:
            s.x += rel_x
            s.y += rel_y

    def draw(self):
        """Make the node graphics object draw itself.
        """
        for s in self._shapes:
            s.draw()
