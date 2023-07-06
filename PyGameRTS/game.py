import sys
from pygame import *
from components import Render, OnClick, Camera, UI, SpriteLoader, Sprite, Collider2D
from uiElements import TextUI, Icon
from tile import Chunk


class Game:
    FPS = 60
    clock = time.Clock()
    screen = None
    size = None
    scroll_speed = 150
    mouse_scroll = True
    draw_hit_box = False
    fpsUIText = None
    fpsUIBG = None

    def __init__(self, size):
        init()
        Game.screen = display.set_mode([size[0], size[1]])
        Render.screen = Game.screen
        Render.clip_rect = Rect(1, 1, size[0]-2, size[1]-2)
        Render.screen.set_clip(Render.clip_rect)
        Game.size = Vector2(size[0], size[1])
        Game.fpsUIText = TextUI()
        Game.fpsUIText.components["text"].color = (100, 255, 100)
        Game.fpsUIText.components["text"].flags = 1
        Game.fpsUIBG = Icon()
        Game.fpsUIBG.addComponent(Sprite("black", (0, 0)))

    def run(self):
        press_up = False
        press_down = False
        press_left = False
        press_right = False
        show_fps = False
        for s in SpriteLoader.sprites.values():
            s.convert()
        Render.render_frame(Render.ALL)
        while True:
            dt = Game.clock.tick(60) / 1000
            events = event.get([MOUSEBUTTONDOWN, KEYDOWN, KEYUP])
            flags = Render.NONE
            if show_fps:
                Game.FPS = Game.clock.get_fps()
                Game.fpsUIText.components["text"].text = f"{int(Game.FPS)}"
                Game.fpsUIBG.components["sprite"].resize((UI.font_size * 0.67 * 2, UI.font_size * 0.89))
                flags = flags ^ Render.TEXT ^ Render.UI
            elif Game.fpsUIText.components["text"].text != "":
                Game.fpsUIText.components["text"].text = ""
                Game.fpsUIBG.components["sprite"].resize((0, 0))
            for _event in events:
                if _event.type == MOUSEBUTTONDOWN:
                    x, y = _event.pos
                    for s in OnClick.onClickEvents:
                        if "collider2D" in s.parent.components.keys():
                            col = s.parent.components["collider2D"]
                            if col.collide_point(x, y):
                                s()
                                flags = Render.ALL
                                break
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
                    if _event.key == K_F4 and not show_fps: show_fps = True; break
                    if _event.key == K_F4 and show_fps: show_fps = False
            event_ = event.poll()
            while event_.type != NOEVENT:
                if event_.type == QUIT:
                    quit()
                    sys.exit()
                event_ = event.poll()

            x, y = mouse.get_pos()
            view_x, view_y = Chunk.GetViewSize()
            if press_up or (-10 < y < 10 and Game.mouse_scroll):
                if -view_y - 36 + self.size[1] < Camera.pos.y + Game.scroll_speed * dt < -60:
                    Camera.pos.y += Game.scroll_speed * dt
                    flags = Render.ALL
            if press_left or (-10 < x < 10 and Game.mouse_scroll):
                if -view_x + self.size[0] < Camera.pos.x + Game.scroll_speed * dt < -50:
                    Camera.pos.x += Game.scroll_speed * dt
                    flags = Render.ALL
            if press_right or (Game.size.x - 10 < x < Game.size.x + 10 and Game.mouse_scroll):
                if -view_x + self.size[0] < Camera.pos.x - Game.scroll_speed * dt < -50:
                    Camera.pos.x -= Game.scroll_speed * dt
                    flags = Render.ALL
            if press_down or (Game.size.y - 10 < y < Game.size.y + 10 and Game.mouse_scroll):
                if -view_y - 36 + self.size[1] < Camera.pos.y - Game.scroll_speed * dt < -60:
                    Camera.pos.y -= Game.scroll_speed * dt
                    flags = Render.ALL
            Render.render_frame(flags)
            if Game.draw_hit_box:
                for col in Collider2D.colliders:
                    col.draw_hit_box(Game.screen)

            display.flip()
