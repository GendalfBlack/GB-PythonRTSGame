import random as rnd
from mapObject import MapObject
from game import Game
from components import *
from icon import Icon

SpriteLoader()

w = Game((800, 600))

for i in range(30):
    MapObject((rnd.randint(0, 10) * 10, rnd.randint(0, 20) * 10), sprite="tree", size=(100, 100))
MapObject((200, 200), sprite="house", size=(150, 150))

u1 = Icon((100, 100), sprite="grass", size=(50, 50))
u1.addComponent(OnClick(u1))
u1.components["onClick"].addEvent(lambda: print("hello"))

w.run()
