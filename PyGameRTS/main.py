import sys
from pygame import *
from gameObject import *

init()
SpriteLoader()

screen = display.set_mode((800,600))

while True:
    for _event in event.get():
        if _event.type == QUIT:
            quit()
            sys.exit()
