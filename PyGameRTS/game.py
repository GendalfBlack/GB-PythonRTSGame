import sys
from pygame import *
from components import Render, OnClick


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
                if _event.type == MOUSEBUTTONDOWN:
                    x,y = _event.pos
                    for s in OnClick.onClickEvents:
                        sx, sy = s.parent.pos[0], s.parent.pos[1]
                        sw = s.parent.components["sprite"].size[0]
                        sh = s.parent.components["sprite"].size[1]
                        if Rect(sx, sy, sw, sh).collidepoint(x, y):
                            s()
                if _event.type == QUIT:
                    quit()
                    sys.exit()

            Render.render_sprites(Game.screen)

            display.flip()
