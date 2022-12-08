from components import *
import random as rnd


class Tile(Background):
    tiles = {}

    def __init__(self, pos=(0, 0), cord=(0, 0)):
        super().__init__(pos)
        Tile.tiles[f"{pos[0]},{pos[1]}"] = self
        self.cord = cord

    @staticmethod
    def getRandom():
        return rnd.choice(list(Tile.tiles.values()))
