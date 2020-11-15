from pynode.nodes import node
from pynode.gui import gui
import pyglet
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    node1 = node.Node('Super Node', (['in1', 'in2', 'in3']), ['out2'])
    node2 = node.Node('Super Node 20', (['in1', 'in2']), ['out2'])
    node3 = node.Node('Sup', (['in1', 'in2', 'in3', 'in4', 'in5', 'in6']), ['out2'])
    gui = gui.Gui([node1, node2, node3])
    pyglet.app.run()
