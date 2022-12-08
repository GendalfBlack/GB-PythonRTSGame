from components import *


class MapObject(GameObject):
    def __init__(self, tile, **args):
        self.tile = tile
        x, y = tile.transform.pos.x, tile.transform.pos.y - 25
        super().__init__((x, y))
        if "name" in args.keys(): self.name = args["name"]
        else: self.name = "New GameObject"

