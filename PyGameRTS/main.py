import random as rnd
from gameObject import GameObject
from gameClass import Game
from spriteComponent import SpriteLoader
from uiIcon import UIIcon

SpriteLoader()

w = Game((800, 600))

for i in range(30):
    GameObject((rnd.randint(0,10)*10,rnd.randint(0,20)*10), name="tree", sprite="tree", size=(100,100))
GameObject((200,200), name="house", sprite="house", size=(150,150))

UIIcon((100,100), sprite="grass", size=(50,50))

w.run()