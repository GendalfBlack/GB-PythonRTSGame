from components import *


class GameObject2D(GameObject):
    clicked = None

    def __init__(self, pos=(0,0), **args):
        super().__init__()
        self.pos = pos
        if "name" in args.keys(): self.name = args["name"]
        else: self.name = "New GameObject"
        if "sprite" in args.keys(): self.components["sprite"] = SpriteComponent(args["sprite"], self)
        else: self.components["sprite"] = None
        if "size" in args.keys() and "sprite" in self.components.keys():
            self.components["sprite"].resize(args["size"])

    def addComponent(self, other):
        if isinstance(other, Component): self.components[other.name] = other
