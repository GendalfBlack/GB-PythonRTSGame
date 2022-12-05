import sys
from pygame import *
from components import Render, OnClick, Camera


class Game:
    screen = None
    size = None

    def __init__(self, size):
        init()
        Game.screen = display.set_mode(size)
        Game.size = Vector2(size[0], size[1])

    @staticmethod
    def run():
        press_up = False
        press_down = False
        press_left = False
        press_right = False
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
                if _event.type == KEYDOWN:
                    if _event.key == K_w: press_up = True
                    if _event.key == K_a: press_left = True
                    if _event.key == K_s: press_down = True
                    if _event.key == K_d: press_right = True
                if _event.type == KEYUP:
                    press_up = False; press_left = False; press_down = False; press_right = False
                if _event.type == QUIT:
                    quit()
                    sys.exit()

            x, y = mouse.get_pos()
            if press_up or 0 < y < 10:
                Camera.pos.y += 1
            if press_left or 0 < x < 10:
                Camera.pos.x += 1
            if press_right or Game.size.x - 10 < x < Game.size.x:
                Camera.pos.x -= 1
            if press_down or Game.size.y - 10 < y < Game.size.y:
                Camera.pos.y -= 1

            Render.render_sprites(Game.screen)

            display.flip()
