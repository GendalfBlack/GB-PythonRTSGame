import random as rnd

from game import Game
from components import *

from uiElements import Icon, TextUI
from tile import Tile
from mapObject import MapObject

SpriteLoader()

w,h = 800,600

root = Game((w, h))

for i in range(w//50):
    for j in range(h//50):
        t = Tile((i*50,j*50))
        t.addComponent(Sprite("grass", (50,50)))

u1 = Icon((w-150, h-150))
u1.addComponent(Sprite("house", (100,100)))

t1 = TextUI((w-100, h-50))
t1.addComponent(Text(""))


def showInfo(obj):
    global u1
    u1.components["sprite"].swap(obj.components["sprite"].sprite)
    t1.components["text"].text = "100/100"


for i in range(30):
    m = MapObject((rnd.randint(0, 10) * 10, rnd.randint(0, 20) * 10))
    m.addComponent(Sprite("tree", (100, 100)))
    m.addComponent(OnClick())
    m.components["onClick"].addEvent(lambda: showInfo(m))
m2 = MapObject((200, 200))
m2.addComponent(Sprite("house", (150, 150)))
m2.addComponent(OnClick())
m2.components["onClick"].addEvent(lambda: showInfo(m2))

root.run()
