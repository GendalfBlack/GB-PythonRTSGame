import random as rnd
from gameObject import *
from gameClass import Game

SpriteLoader()

w = Game((800, 600))


for i in range(8):
    for j in range(6):
        GameObject((i*100, j*100),sprite="grass", size=(100,100))

for i in range(30):
    GameObject((rnd.randint(0,700),rnd.randint(0,500)), name="tree", sprite="tree", size=(100,100))
GameObject((200,200), name="tree", sprite="house", size=(150,150))

w.run()