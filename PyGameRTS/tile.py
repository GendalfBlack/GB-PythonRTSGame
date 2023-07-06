from components import *
import random as rnd


class Tile(Background):
    SOUTH = 2
    WEST = 3
    NORTH = 0
    EAST = 1
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
            self.addComponent(Sprite(value, (100, 100)))

    def __init__(self, pos=(0, 0), cord=(0, 0)):
        super().__init__(pos)
        Tile.tiles[f"{cord[0]},{cord[1]}"] = self
        self.id = f"{cord[0]},{cord[1]}"
        self.cord = cord
        self.selected = False
        self.sprites = []
        self.possible = []
        self.sides = ["", "", "", ""]
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
        self.selected = True

    def Collapse(self):
        if self.isCollapsed:
            return self
        for n in self.neighbours:
            if n is None:
                continue
            if n.Sprite is None:
                continue
            i = self.neighbours.index(n) ^ 2
            self.sides[i ^ 2] = n.Sprite.sides[i]
            self.possible.clear()
            for s in self.sprites:
                self.possible.append(s)
            j = 0
            while j < len(self.possible):
                for i in range(4):
                    if self.sides[i] != "":
                        if self.possible[j].split('_')[i] != self.sides[i]:
                            self.possible.remove(self.possible[j])
                            j -= 1
                            break
                j += 1
        if len(self.possible) == 0:
            self.Sprite = rnd.choice(self.sprites)
        else:
            self.Sprite = rnd.choice(self.possible)
            self.possible.clear()
        self.isCollapsed = True
        for n in self.neighbours:
            self.UpdateNeighbour(n)
        return self

    def UpdateNeighbour(self, n):
        if n is None:
            return
        if n.isCollapsed:
            return
        i = self.neighbours.index(n)
        n.UpdateSprites(self.Sprite.sides[i], i ^ 2)

    def UpdateSprites(self, material, side):
        self.possible.clear()
        for s in self.sprites:
            if s.split('_')[side] == material:
                self.possible.append(s)
        self.Collapse()


class Chunk:
    sum_width = 0
    sum_height = 0

    def __init__(self, pos=(0, 0)):
        self.pos = pos
        self.width = 3
        self.height = 3
        self.center = (pos[0] * self.width - pos[1] * self.width, pos[0] * self.height + pos[1] * self.height)
        self.tiles = []
        self.next = None

    def Generate(self):
        i = self.center[0]
        j = self.center[1] - 2
        for y in range(self.height):
            for x in range(self.width):
                dx = self.center[1] * 50 + self.center[0] * 50
                dy = self.center[1] * 25 - self.center[0] * 25
                t = Tile((x * 100 + dx, y * 50 + dy), (i, j))  # even
                t2 = Tile((x * 100 + 50 + dx, y * 50 + 25 + dy), (i, j + 1))  # odd
                for s in SpriteLoader.tiles.keys():
                    t.sprites.append(s)
                    t2.sprites.append(s)
                    t.SpriteLeft += 1
                    t2.SpriteLeft += 1
                '''t.addComponent(OnClick())
                t2.addComponent(OnClick())
                t.components["onClick"].addEvent(t.selectTile)
                t2.components["onClick"].addEvent(t2.selectTile)'''
                t.addComponent(Collider2D())
                t2.addComponent(Collider2D())
                t.components["collider2D"].points = [(0, 60), (50, 35), (100, 60), (50, 85)]
                t2.components["collider2D"].points = [(0, 60), (50, 35), (100, 60), (50, 85)]
                self.tiles.append(t)
                self.tiles.append(t2)
                i += 1
                j += 1
            j -= 2
            i -= 4

    def CalculateNeighbours(self):
        for tile in self.tiles:
            xy = tile.id.split(',')
            x, y = int(xy[0]), int(xy[1])
            north = f"{x},{y - 1}"
            if north in Tile.tiles.keys():
                tile.neighbours[Tile.NORTH] = Tile.tiles[north]
            south = f"{x},{y + 1}"
            if south in Tile.tiles.keys():
                tile.neighbours[Tile.SOUTH] = Tile.tiles[south]
            east = f"{x + 1},{y}"
            if east in Tile.tiles.keys():
                tile.neighbours[Tile.EAST] = Tile.tiles[east]
            west = f"{x - 1},{y}"
            if west in Tile.tiles.keys():
                tile.neighbours[Tile.WEST] = Tile.tiles[west]

    def Collapse(self):
        if (self.next is None or self.next.isCollapsed) and len(self.tiles) > 0:
            t = rnd.choice(self.tiles)
            t.Collapse()
            self.tiles.remove(t)
        else:
            Tile.next.Collapse()

    @staticmethod
    def GetViewSize():
        return Chunk.sum_width * 100 * 3, Chunk.sum_height * 50 * 3
