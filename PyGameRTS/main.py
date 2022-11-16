import random as rnd
from gameObject import GameObject2D
from gameClass import Game
from components import *
from uiIcon import UIIcon

SpriteLoader()

w = Game((800, 600))

for i in range(30):
    GameObject2D((rnd.randint(0,10)*10,rnd.randint(0,20)*10), sprite="tree", size=(100,100))
GameObject2D((200,200), sprite="house", size=(150,150))

u1 = UIIcon((100,100), sprite="grass", size=(50,50))
u1.addComponent(OnClickComponent(u1))
u1.components["onClick"].addEvent(lambda: print("hello"))


w.run()