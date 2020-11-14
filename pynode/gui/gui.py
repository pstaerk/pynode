import pyglet

class Gui(pyglet.window.Window):
    """Gui baseclass, a simple node renderer Implemented in pyglet."""
    def __init__(self, nodes):
        """Initializes a display with the possibility of adding a list
        of nodes.

        :nodes: List of node classes that one can add.
        """
        super(Gui, self).__init__()
        self.label = pyglet.text.Label('Hello world', x=self.width//2, y=self.height//2)

    def on_draw(self):
        self.clear()
        self.label.draw()
