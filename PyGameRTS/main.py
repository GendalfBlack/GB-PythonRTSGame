
from gameObject import *
from gameClass import Game

SpriteLoader()

w = Game()

g = GameObject((0,0), name="tree", sprite="tree", size=(100,100))
GameObject((200,200), name="tree", sprite="house", size=(100,100))

w.run()