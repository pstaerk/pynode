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
        self._mainbatch = pyglet.graphics.Batch()
        self._nodebatch = pyglet.graphics.OrderedGroup(0)
        self._labelbatch = pyglet.graphics.OrderedGroup(1)
        self.create_nodes(nodes)
        self.drawing = False
        self._current_line = None

    def create_nodes(self, nodes):
        """Create pyglet instances of the nodes.

        :nodes: list of node objects.
        """
        for n in nodes:
            tn = NodeGraphics(n, (100, 200), self._mainbatch, self._nodebatch, self._labelbatch)
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
            for n in self._nodes:
                # check if and what sort of type is the connector that possibly is clicked on
                cnct_type, is_clicked = n.check_click_location(x, y) 
                if is_clicked:
                    # create the line to draw
                    self.line_draw_start(is_clicked, x, y)
        else:
            # Draw!
            self.update_drawing(x, y)

    def line_draw_start(self, start_rect, x, y):
        """Handle the drawing of a new line.
        """
        self.drawing = True
        print('Am in the draw starting')
        line = create_line_starting_from_rect(start_rect, self._mainbatch, self._nodebatch, x, y)
        self._current_line = line

    def update_drawing(self, x, y):
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
