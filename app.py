from pynode.nodes import node
from pynode.gui import gui
import pyglet

if __name__ == "__main__":
    node = node.Node('Super Node', (['in1', 'in2', 'in3']), ['out2'])
    gui = gui.Gui([node])
    pyglet.app.run()
