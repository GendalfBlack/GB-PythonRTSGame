import random as rnd
import sys
from game import Game
from components import *
from uiElements import *
from tile import Tile, Chunk
from mapObject import MapObject

sys.setrecursionlimit(1000)

SpriteLoader()

w, h = 800, 600

root = Game((w, h))
chunks = []
for i in range(0, 10):
    for j in range(0, 10):
        c = Chunk((i, j))
        c.Generate()
        chunks.append(c)
        if i == 0: Chunk.sum_height += 1
    Chunk.sum_width += 1
for c in chunks:
    c.CalculateNeighbours()
    c.Collapse()

u1 = Icon((w - 150, h - 150))
u1.addComponent(Sprite("house", (100, 100)))

t1 = TextUI((w - 100, h - 50))


def addTree():
    tree = MapObject(Tile.getRandom())
    tree.addComponent(Sprite("tree", (100, 100)))
    tree.addComponent(OnClick())
    tree.components["onClick"].addEvent(showInfo, tree)
    tree.addComponent(Collider2D())
    tree.components["collider2D"].points = [(0, 50), (50, 0), (100, 50), (50, 100)]


b1 = Button((w - 150, h - 250))
b1.components["onClick"].addEvent(addTree)
b1.addComponent(Collider2D())

last = None

def showInfo(obj):
    global last
    if last is not None:
        last.tile.selectTile()
    u1.components["sprite"].swap(obj.components["sprite"].image)
    t1.components["text"].text = "100/100"
    obj.tile.selectTile()
    last = obj


for i in range(25):
    m = MapObject(Tile.getRandom())
    m.addComponent(Sprite("tree", (100, 100)))
    m.addComponent(OnClick())
    m.components["onClick"].addEvent(showInfo, m)
    m.addComponent(Collider2D())
    m.components["collider2D"].points = [(0, 50), (50, 0), (100, 50), (50, 100)]
'''
m2 = MapObject(Tile.getRandom())
m2.addComponent(Sprite("house", (150, 150)))
m2.addComponent(OnClick())
m2.components["onClick"].addEvent(lambda: showInfo(m2))
m2.addComponent(Collider2D())'''

root.run()
