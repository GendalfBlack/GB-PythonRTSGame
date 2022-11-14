import random as rnd
from gameObject import GameObject
from gameClass import Game
from spriteComponent import SpriteLoader

SpriteLoader()

w = Game((800, 600))

for i in range(30):
    GameObject((rnd.randint(0,7)*100,rnd.randint(0,5)*100), name="tree", sprite="tree", size=(100,100))
GameObject((200,200), name="house", sprite="house", size=(150,150))

w.run()