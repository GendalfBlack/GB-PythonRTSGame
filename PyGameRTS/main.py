import random as rnd

from game import Game
from components import *

from uiElements import *
from tile import Tile
from mapObject import MapObject

SpriteLoader()

w,h = 800,600

root = Game((w, h))

for i in range(w//100):
    for j in range(h//25):
        if j % 2 ==0:
            t = Tile((i * 100, j * 25), (i, j))
        else:
            t = Tile((i * 100 + 50, j * 25), (i, j))
        t.addComponent(Sprite("grass", (100,100)))

u1 = Icon((w-150, h-150))
u1.addComponent(Sprite("house", (100,100)))

t1 = TextUI((w-100, h-50))
t1.addComponent(Text(""))


def addTree():
    tree = MapObject(Tile.getRandom())
    tree.addComponent(Sprite("tree", (100, 100)))
    tree.addComponent(OnClick())
    tree.components["onClick"].addEvent(lambda: showInfo(tree))


b1 = Button((w-150, h-250))
b1.components["onClick"].addEvent(addTree)


def showInfo(obj):
    u1.components["sprite"].swap(obj.components["sprite"].sprite)
    t1.components["text"].text = "100/100"


for i in range(1):
    m = MapObject(Tile.getRandom())
    m.addComponent(Sprite("tree", (100, 100)))
    m.addComponent(OnClick())
    m.components["onClick"].addEvent(lambda: showInfo(m))

m2 = MapObject(Tile.getRandom())
m2.addComponent(Sprite("house", (150, 150)))
m2.addComponent(OnClick())
m2.components["onClick"].addEvent(lambda: showInfo(m2))

root.run()
