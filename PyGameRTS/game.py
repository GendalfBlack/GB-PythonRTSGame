import sys
from pygame import *
from Components.RenderComponent import Render
from Components.UIComponent import UI
from Components.SpriteLoaderComponent import SpriteLoader
from Components.SpriteComponent import Sprite
from Components.CameraComponent import Camera
from Components.Collider2DComponent import Collider2D
from Components.OnClickComponent import OnClick
from uiElements import TextUI, Icon
from tile import Chunk


class Game:
    FPS = 60
    UI_rect = (1, 26, -202, -2)
    clock = time.Clock()
    screen = None
    size = None
    scroll_speed = 0.15
    mouse_scroll = True
    draw_hit_box = False
    fpsUIText = None
    fpsUIBG = None

    press_up = False
    press_down = False
    press_left = False
    press_right = False
    show_fps = False

    flags = Render.NONE

    def __init__(self, size):
        init()
        Game.screen = display.set_mode([size[0], size[1]])
        Render.screen = Game.screen
        Render.clip_rect = \
            Rect(1 + Game.UI_rect[0],
                 1 + Game.UI_rect[1],
                 size[0] + Game.UI_rect[2],
                 size[1] + Game.UI_rect[3])
        Game.size = Vector2(size[0], size[1])
        Game.fpsUIText = TextUI()
        Game.fpsUIText.components["text"].color = (100, 255, 100)
        Game.fpsUIText.components["text"].flags = 1
        Game.fpsUIBG = Icon()
        Game.fpsUIBG.addComponent(Sprite("black", (0, 0)))

    def EventHandler(self):
        events = event.get()
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
                if _event.key == K_w: Game.press_up = True
                if _event.key == K_a: Game.press_left = True
                if _event.key == K_s: Game.press_down = True
                if _event.key == K_d: Game.press_right = True
                if _event.key == K_F3: Game.draw_hit_box = True
            if _event.type == KEYUP:
                if _event.key == K_w: Game.press_up = False
                if _event.key == K_a: Game.press_left = False
                if _event.key == K_s: Game.press_down = False
                if _event.key == K_d: Game.press_right = False
                if _event.key == K_F3: Game.draw_hit_box = False
                if _event.key == K_F4 and not Game.show_fps: Game.show_fps = True; break
                if _event.key == K_F4 and Game.show_fps: Game.show_fps = False
            if _event.type == QUIT:
                quit()
                sys.exit()

    def CameraMovement(self, dt):
        x, y = mouse.get_pos()
        view_x, view_y = Chunk.GetViewSize()
        if Game.press_up or (-10 < y < 10 and Game.mouse_scroll):
            if -view_y - 36 + self.size[1] < Camera.pos.y + Game.scroll_speed * dt < -60:
                Camera.pos.y += Game.scroll_speed * dt
                Game.flags = Render.ALL
        if Game.press_left or (-10 < x < 10 and Game.mouse_scroll):
            if -view_x + self.size[0] < Camera.pos.x + Game.scroll_speed * dt < -50:
                Camera.pos.x += Game.scroll_speed * dt
                Game.flags = Render.ALL
        if Game.press_right or (Game.size.x - 10 < x < Game.size.x + 10 and Game.mouse_scroll):
            if -view_x + self.size[0] + Game.UI_rect[2] < Camera.pos.x - Game.scroll_speed * dt < -50:
                Camera.pos.x -= Game.scroll_speed * dt
                Game.flags = Render.ALL
        if Game.press_down or (Game.size.y - 10 < y < Game.size.y + 10 and Game.mouse_scroll):
            if -view_y - 36 + self.size[1] < Camera.pos.y - Game.scroll_speed * dt < -60:
                Camera.pos.y -= Game.scroll_speed * dt
                Game.flags = Render.ALL

    @staticmethod
    def ShowFPS():
        if Game.show_fps:
            Game.FPS = Game.clock.get_fps()
            Game.fpsUIText.components["text"].text = f"{int(Game.FPS)}"
            Game.fpsUIBG.components["sprite"].resize((UI.font_size * 0.67 * 2, UI.font_size * 0.89))
            Game.flags = Game.flags ^ Render.TEXT ^ Render.UI
        elif Game.fpsUIText.components["text"].text != "":
            Game.fpsUIText.components["text"].text = ""
            Game.fpsUIBG.components["sprite"].resize((0, 0))

    def run(self):
        for s in SpriteLoader.sprites.values():
            s.convert()
        Render.render_frame(Render.ALL)
        while True:
            dt = Game.clock.tick(60)
            Game.ShowFPS()
            self.EventHandler()
            self.CameraMovement(dt)
            Render.render_frame(Game.flags)
            if Game.draw_hit_box:
                for col in Collider2D.colliders:
                    col.draw_hit_box(Game.screen)

            display.flip()
