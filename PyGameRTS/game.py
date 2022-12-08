import sys
from pygame import *
from components import Render, OnClick, Camera, UI


class Game:
    FPS = 60
    clock = time.Clock()
    screen = None
    size = None
    scroll_speed = 100
    draw_hit_box = False

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
            dt = Game.clock.tick()/1000
            events = event.get()
            for _event in events:
                if _event.type == MOUSEBUTTONDOWN:
                    x,y = _event.pos
                    for s in OnClick.onClickEvents:
                        if not isinstance(s.parent, UI):
                            sx, sy = s.parent.transform.pos.x + Camera.pos.x, \
                                     s.parent.transform.pos.y + Camera.pos.y
                        else:
                            sx, sy = s.parent.transform.pos.x, s.parent.transform.pos.y
                        sw = s.parent.transform.size.x
                        sh = s.parent.transform.size.y
                        if Rect(sx, sy, sw, sh).collidepoint(x, y):
                            s()
                if _event.type == KEYDOWN:
                    if _event.key == K_w: press_up = True
                    if _event.key == K_a: press_left = True
                    if _event.key == K_s: press_down = True
                    if _event.key == K_d: press_right = True
                    if _event.key == K_F3: Game.draw_hit_box = True
                if _event.type == KEYUP:
                    if _event.key == K_w: press_up = False
                    if _event.key == K_a: press_left = False
                    if _event.key == K_s: press_down = False
                    if _event.key == K_d: press_right = False
                    if _event.key == K_F3: Game.draw_hit_box = False
                if _event.type == QUIT:
                    quit()
                    sys.exit()

            x, y = mouse.get_pos()
            if press_up or 0 < y < 10:
                Camera.pos.y += Game.scroll_speed * dt
            if press_left or 0 < x < 10:
                Camera.pos.x += Game.scroll_speed * dt
            if press_right or Game.size.x - 10 < x < Game.size.x:
                Camera.pos.x -= Game.scroll_speed * dt
            if press_down or Game.size.y - 10 < y < Game.size.y:
                Camera.pos.y -= Game.scroll_speed * dt

            Render.render_sprites(Game.screen)

            if Game.draw_hit_box:
                for s in OnClick.onClickEvents:
                    if not isinstance(s.parent, UI):
                        sx, sy = s.parent.transform.pos.x + Camera.pos.x, \
                                 s.parent.transform.pos.y + Camera.pos.y
                    else:
                        sx, sy = s.parent.transform.pos.x, s.parent.transform.pos.y
                    sw = s.parent.transform.size.x
                    sh = s.parent.transform.size.y
                    draw.line(Game.screen, (255, 0, 0), [sx, sy], [sx + sw, sy], 2)
                    draw.line(Game.screen, (255, 0, 0), [sx, sy], [sx, sy + sh], 2)
                    draw.line(Game.screen, (255, 0, 0), [sx, sy + sh], [sx + sw, sy + sh], 2)
                    draw.line(Game.screen, (255, 0, 0), [sx + sw, sy], [sx + sw, sy + sh], 2)

            display.flip()
