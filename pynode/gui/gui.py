import pyglet
from pynode.gui.nodegraphics import NodeGraphics
import logging 

class Gui(pyglet.window.Window):
    """Gui baseclass, a simple node renderer Implemented in pyglet."""
    def __init__(self, nodes):
        """Initializes a display with the possibility of adding a list
        of nodes.

        :nodes: List of node classes that one can add.
        """
        super(Gui, self).__init__()
        self._nodes = []
        self._lines = []
        self._mainbatch = pyglet.graphics.Batch()
        self._nodebatch = pyglet.graphics.OrderedGroup(0)
        self._labelbatch = pyglet.graphics.OrderedGroup(1)
        self.create_nodes(nodes)
        self._starting_node = None # for keeping track of the starting point
        self._starting_type = None # type of the docker for keeping track of the starting point
        self._starting_nr   = None # starting number of the starting docker
        self.drawing = False
        self._current_line = None

    def create_nodes(self, nodes):
        """Create pyglet instances of the nodes.

        :nodes: list of node objects.
        """
        for i, n in enumerate(nodes):
            tn = NodeGraphics(n, (100+i*200, 200), self._mainbatch, self._nodebatch, self._labelbatch)
            self._nodes.append(tn)

    def on_draw(self):
        self.clear()
        self._mainbatch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Tell the window what to do when the mouse is pressed.
        """
        pass # currently nothing has to be done.

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """What to do when mouse is dragged.
        """
        if not self.drawing:
            cnct_type, is_clicked, start_node, j = self.check_if_on_node_docker(x, y)
            if is_clicked:
                # create the line to draw
                self.line_draw_start(is_clicked, x, y, cnct_type, start_node, j)
        else:
            # Draw!
            self.update_line(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        """What to do when the mouse is released again.
        """
        if self.drawing: # check if we were drawing a line
            # check if line is now on top of docking of correct type
            cnct_type, is_clicked, end_node, j = self.check_if_on_node_docker(x, y)
            if is_clicked:
                self.stop_line_on_docker(cnct_type, end_node, j)
            else: # Stop drawing the line and delete it
                self.delete_current_line()

    def delete_current_line(self):
        """Delete the line which is currently being drawn.
        :returns: TODO

        """
        line = self._current_line
        line.delete()
        self._current_line = None
        self.drawing = False

    def stop_line_on_docker(self, cnct_type, stop_node, input_nr):
        """Code handling the possible end point of the line drawing.
        Needs to know the type of the docker that the line ostensibly should end
        on, given by cnct_type ('in' or 'out)'.
        """
        # check if docker is eligible to be ended on, i.e. another node, in to out
        # or out to in
        if stop_node != self._starting_node and cnct_type != self._starting_type:
            logging.info('Keeping line')
            self._lines.append(self._current_line)
            # TODO check if the stop is the incoming !
            logging.warning('Not checking if incoming')
            stop_node._node.add_edge(input_nr, self._starting_node)
            stop_node.add_line(self._current_line, 'end')
            self._starting_node.add_line(self._current_line, 'start') # this needs to be checked!
            self._starting_node._node.add_edge(self._starting_nr, self._current_line)
            logging.debug(stop_node._node._incoming_edges)
            self._starting_node = None
            self._starting_type = None
            self._current_line = None
            self.drawing = False # Nothing else has to be done as the line stays
            # Add the link:
        else:
            self.delete_current_line()

    def check_if_on_node_docker(self, x, y):
        """Check if mouse is on any "clickable" on the nodes. Returns the type 
        of the docker ('in'/'out'). The rectangle object or false, the node and
        the number/position of the docker in the input/output list.
        """
        tmp_n = None
        for i, n in enumerate(self._nodes):
            # check if and what sort of type is the connector that possibly is clicked on
            cnct_type, is_clicked, j = n.check_click_location(x, y) 
            if is_clicked: 
                tmp_n = n
                break
        return cnct_type, is_clicked, n, j

    def line_draw_start(self, start_rect, x, y, cnct_type, start_node, start_nr):
        """Handle the drawing of a new line.
        """
        self.drawing = cnct_type
        line = create_line_starting_from_rect(start_rect, self._mainbatch, self._nodebatch, x, y)
        self._current_line = line
        self._starting_type = cnct_type
        self._starting_node = start_node
        self._starting_nr   = start_nr

    def update_line(self, x, y):
        """Update the current line and draw it according to how much the mouse has moved.
        """
        if not self.drawing:
            logging.error('You have attempted to draw a line, when the window is not in drawing mode.')
        self._current_line.x2 = x
        self._current_line.y2 = y
        self._mainbatch.draw()


def create_line_starting_from_rect(rect, drawbatch, group, x, y):
    """Draw a line starting from the rectangle rect. Make sure it is part of the batch drawbatch
    and assigned to the drawgroup group.
    """
    startpointx = rect.x + rect.width/2
    startpointy = rect.y + rect.height/2
    line = pyglet.shapes.Line(startpointx, startpointy, x, y, batch=drawbatch, group=group) 
    print(f'line is {line}')
    return line
