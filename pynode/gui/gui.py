import pyglet
from pynode.gui.nodegraphics import NodeGraphics

class Gui(pyglet.window.Window):
    """Gui baseclass, a simple node renderer Implemented in pyglet."""
    def __init__(self, nodes):
        """Initializes a display with the possibility of adding a list
        of nodes.

        :nodes: List of node classes that one can add.
        """
        super(Gui, self).__init__()
        self._nodes = []
        self.create_nodes(nodes)

    def create_nodes(self, nodes):
        """Create pyglet instances of the nodes.

        :nodes: list of node objects.
        """
        print(nodes)
        for n in nodes:
            tn = NodeGraphics(n, (100, 200))
            self._nodes.append(tn)

    def on_draw(self):
        self.clear()
        for n in self._nodes:
            print(f'Drawing node {n}')
            n.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Tell the window what to do when the mouse is pressed.
        """
        pass # currently nothing has to be done.

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """What to do when mouse is dragged.
        """
        pass # currently nothing has to be done.
