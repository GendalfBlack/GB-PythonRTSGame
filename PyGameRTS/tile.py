from components import *
import random as rnd


class Tile(Background):
    SOUTH = 0
    WEST = 1
    NORTH = 2
    EAST = 3
    tiles = {}

    @property
    def SpriteLeft(self):
        return self._value

    @SpriteLeft.setter
    def SpriteLeft(self, value):
        self._value = value

    @property
    def Sprite(self):
        if "sprite" in self.components.keys():
            return self.components["sprite"]

    @Sprite.setter
    def Sprite(self, value):
        if "sprite" in self.components.keys():
            self.components["sprite"].swap(value.sprite)
        else:
            self.addComponent(Sprite(value.sprite_name, (100, 100)))

    def __init__(self, pos=(0, 0), cord=(0, 0)):
        super().__init__(pos)
        Tile.tiles[f"{pos[0]},{pos[1]}"] = self
        self.id = f"{cord[0]},{cord[1]}"
        self.cord = cord
        self.selected = False
        self.sprites = []
        self._value = 0
        self.isCollapsed = False
        self.neighbours = [None, None, None, None]

    @staticmethod
    def getRandom():
        return rnd.choice(list(Tile.tiles.values()))

    def selectTile(self, color=(255, 0, 0)):
        if not self.components["collider2D"]:
            return
        if self.selected:
            Render.remove_rectangle(self.id)
            self.selected = False
            return

        Render.draw_rectangle(self.id, self.components["collider2D"].points, color)
        print(self.id)
        self.selected = True

    def Collapse(self):
        if self.isCollapsed:
            return self
        if len(self.sprites) == 0:
            self.Sprite = Sprite("grass", (100,100))
            return self

        self.Sprite = rnd.choice(self.sprites)
        self.sprites.clear()
        self.isCollapsed = True
        for n in self.neighbours:
            self.UpdateNeighbour(n)
        return self

    def UpdateNeighbours(self, n):
        if not n:
            return
        if n.isCollapsed:
            return
        i = self.neighbours.index(n)
        if i == Tile.SOUTH:
            n.UpdateSprites(self.Sprite.sides[i], Tile.NORTH)
        elif i == Tile.EAST:
            n.UpdateSprites(self.Sprite.sides[i], Tile.WEST)
        elif i == Tile.NORTH:
            n.UpdateSprites(self.Sprite.sides[i], Tile.SOUTH)
        else:
            n.UpdateSprites(self.Sprite.sides[i], Tile.EAST)

    def UpdateSprites(self, material, side):
        i = 0
        while i < len(self.sprites):
            if self.sprites[i].sides[side] != material:
                self.sprites.remove(self.sprites[i])
                self._value -= 1
                i -= 1
            i += 1


class Chunk:
    update_queue = []

    def __init__(self):
        self.width = 10
        self.height = 10
        self.tiles = []
        self.sides = [[], [], [], []]
        self.neighbours = [None, None, None, None]

    def Generate(self):
        for y in range(self.height):
            for x in range(self.width):
                t = Tile((x * 50, y * 50 + (x % 2) * 25), (x, y))
                for s in SpriteLoader.tiles.keys():
                    t.sprites.append(Sprite(s, (100, 100)))
                    t.SpriteLeft += 1
                self.tiles.append(t)
                t.addComponent(OnClick())
                t.components["onClick"].addEvent(t.selectTile)
                t.addComponent(Collider2D())
                t.components["collider2D"].points = [(0, 60), (50, 35), (100, 60), (50, 85)]
        self.CalculateNeighbours()

    def CalculateNeighbours(self):
        for y in range(self.height):
            for x in range(self.width):
                go = self.tiles[y * self.height + x]
                if x == 0 and y == 0:
                    self.tiles[(y) * self.height + (x + 1)].neighbours[Tile.SOUTH] = go
                elif x == self.width - 1 and y == self.height - 1:
                    self.tiles[(y) * self.height + (x - 1)].neighbours[Tile.NORTH] = go
                elif x == 0 and y == self.height - 1:
                    self.tiles[(y - 1) * self.height + (x + 1)].neighbours[Tile.EAST] = go
                    self.tiles[(y) * self.height + (x + 1)].neighbours[Tile.SOUTH] = go
                elif x == self.width - 1 and y == 0:
                    self.tiles[(y - 1) * self.height + (x - 1)].neighbours[Tile.NORTH] = go
                    self.tiles[(y) * self.height + (x - 1)].neighbours[Tile.WEST] = go
                else:
                    if x % 2 == 0:
                        if x == 0:
                            self.tiles[(y-1) * self.height + (x + 1)].neighbours[Tile.EAST] = go
                            self.tiles[(y) * self.height + (x + 1)].neighbours[Tile.SOUTH] = go
                        elif y == 0:
                            self.tiles[(y) * self.height + (x + 1)].neighbours[Tile.SOUTH] = go
                            self.tiles[(y) * self.height + (x - 1)].neighbours[Tile.WEST] = go
                        else:
                            self.tiles[(y-1) * self.height + (x - 1)].neighbours[Tile.NORTH] = go
                            self.tiles[(y-1) * self.height + (x + 1)].neighbours[Tile.EAST] = go
                            self.tiles[(y) * self.height + (x + 1)].neighbours[Tile.SOUTH] = go
                            self.tiles[(y) * self.height + (x - 1)].neighbours[Tile.WEST] = go
                    else:
                        if x == self.width - 1:
                            self.tiles[(y) * self.height + (x - 1)].neighbours[Tile.NORTH] = go
                            self.tiles[(y+1) * self.height + (x - 1)].neighbours[Tile.WEST] = go
                        elif y == self.height - 1:
                            self.tiles[(y) * self.height + (x + 1)].neighbours[Tile.EAST] = go
                            self.tiles[(y) * self.height + (x - 1)].neighbours[Tile.NORTH] = go
                        else:
                            self.tiles[(y) * self.height + (x - 1)].neighbours[Tile.NORTH] = go
                            self.tiles[(y) * self.height + (x + 1)].neighbours[Tile.EAST] = go
                            self.tiles[(y+1) * self.height + (x + 1)].neighbours[Tile.SOUTH] = go
                            self.tiles[(y+1) * self.height + (x - 1)].neighbours[Tile.WEST] = go

    def Collapse(self):
        while len(self.tiles) > 0:
            t = rnd.choice(self.tiles)
            t.Collapse()
            self.tiles.remove(t)
