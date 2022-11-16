from components import *


class Icon(UI):
    def __init__(self, pos=(0,0), **args):
        super().__init__()
        self.ui = True
        self.pos = pos
        if "sprite" in args.keys(): self.sprite = Sprite(args["sprite"], self)
        else: self.sprite = None
        if "size" in args.keys():
            self.size = args["size"]
            self.sprite.resize(self.size)
        else: self.size = (0,0)

    def addComponent(self, other):
        if isinstance(other, Component): self.components[other.name] = other
