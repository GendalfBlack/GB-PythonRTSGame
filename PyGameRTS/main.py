import random as rnd
from mapObject import MapObject
from game import Game
from components import *
from icon import Icon
from tile import Tile

SpriteLoader()

w = Game((800, 600))

for i in range(800//50):
    for j in range(600//50):
        t = Tile((i*50,j*50))
        t.addComponent(Sprite("grass", (50,50)))

for i in range(30):
    m = MapObject((rnd.randint(0, 10) * 10, rnd.randint(0, 20) * 10))
    m.addComponent(Sprite("tree", (100, 100)))
m2 = MapObject((200, 200))
m2.addComponent(Sprite("house", (150, 150)))

u1 = Icon((100, 100))
u1.addComponent(Sprite("grass", (50,50)))
u1.addComponent(OnClick())
u1.components["onClick"].addEvent(lambda: print("hello"))

w.run()
