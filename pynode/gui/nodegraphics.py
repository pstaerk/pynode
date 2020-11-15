import pyglet
from pynode.gui.utils import distribute_in_length

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
    def __init__(self, node, position):
        """Create a node pyglet object to be displayed on the graphical ui.
        """
        self._node = node # keep track of the node object
        self._x, self._y = position[0], position[1]
        self._shapes = []
        self._create_shapes()

    def _calc_shapes(self):
        """Calculate the relevant dimensions of the box from the number of inputs,
        label etc.
        """
        self._width = MINIMUM_LENGTH
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
                color=NODE_COLOR)
        # Add a label bar above the rectangle
        rect2 = pyglet.shapes.Rectangle(self._x, self._y+self._height, self._width, 
                LABEL_HEIGHT, color=LABEL_COLOR)
        lab = pyglet.text.Label(text=self._node._name, x=self._x, 
                y=self._y+self._height+LABEL_YOFFSET)
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
            hpos = self._x + OUTPUTS_OFFSET + self._width - LENGTH_OUTPUT
            trect = pyglet.shapes.Rectangle(hpos, vpos, LENGTH_OUTPUT, LENGTH_OUTPUT,
                    color=OUTPUT_COLOR)
            self._shapes.append(trect)

            # Place labels
            labx, laby = hpos, vpos, 
            tlab = pyglet.text.Label(inp, x=labx, y=laby, anchor_x='right', align='right')
            self._shapes.append(tlab)
        

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
                    color=INPUT_COLOR)
            self._shapes.append(trect)

            # Place labels
            labx, laby = hpos + LENGTH_INPUT, vpos, 
            tlab = pyglet.text.Label(inp, x=labx, y=laby)
            self._shapes.append(tlab)

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
