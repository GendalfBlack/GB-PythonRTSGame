from Components.TransformComponent import Transform
from Components.ComponentMaster import Component


class ComponentsHolder:
    def __init__(self, pos=(0, 0)):
        self.components = {}
        self.transform = Transform(pos)
        self.addComponent(self.transform)

    def addComponent(self, other):
        if isinstance(other, Component):
            self.components[other.name] = other
            other.parent = self
