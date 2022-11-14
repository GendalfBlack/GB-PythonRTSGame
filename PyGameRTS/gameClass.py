import sys
from pygame import *
from spriteComponent import Render


class Game:
    screen = None

    def __init__(self, size):
        init()
        Game.screen = display.set_mode(size)

    @staticmethod
    def run():
        while True:
            events = event.get()
            for _event in events:
                if _event.type == QUIT:
                    quit()
                    sys.exit()

            Render.render_sprites(Game.screen)

            display.flip()
