import sys
from pygame import *

class Game:
    gameobjects = []
    screen = None
    def __init__(self):
        init()
        Game.screen = display.set_mode((800, 600))

    def run(self):
        while True:
            for _event in event.get():
                if _event.type == QUIT:
                    quit()
                    sys.exit()
            for g in Game.gameobjects:
                g.draw()
            display.flip()