from components import *


class MapObject(GameObject):
    def __init__(self, pos=(0,0), **args):
        super().__init__(pos)
        if "name" in args.keys(): self.name = args["name"]
        else: self.name = "New GameObject"
