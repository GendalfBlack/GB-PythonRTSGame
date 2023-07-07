from Components.SpriteComponent import *
from Components.CameraComponent import Camera
from Components.TextComponents import Text


class Render:
    NONE = 1
    BACKGROUND = 2
    SPRITE = 4
    UI = 8
    TEXT = 16
    OVERLAY = 32
    ALL = 63

    screen = None
    clip_rect = None
    shapes = {}

    @staticmethod
    def draw_rectangle(owner, points, color=(255, 0, 0, 0)):
        if owner not in Render.shapes.keys():
            Render.shapes[owner] = points, color

    @staticmethod
    def remove_rectangle(owner):
        if owner in Render.shapes.keys():
            Render.shapes.pop(owner)

    @staticmethod
    def render_frame(flags=NONE):
        Render.screen.set_clip(Render.clip_rect)
        if flags & Render.BACKGROUND:
            for s in Sprite.background_sprites:
                x, y = s.parent.transform.pos.x, s.parent.transform.pos.y
                if 800 - Camera.pos.x > x > Camera.pos.x and 600 - Camera.pos.y > y > Camera.pos.y:
                    Render.screen.blit(s.image, (x + Camera.pos.x, y + Camera.pos.y))
        if flags & Render.SPRITE:
            for s in Sprite.game_sprites:
                x, y = s.parent.transform.pos.x, s.parent.transform.pos.y
                if 800 - Camera.pos.x > x > Camera.pos.x and 600 - Camera.pos.y > y > Camera.pos.y:
                    Render.screen.blit(s.image, (x + Camera.pos.x, y + Camera.pos.y))
        Render.screen.set_clip(None)
        if flags & Render.UI:
            for s in Sprite.ui_sprites:
                x, y = s.rect.x, s.rect.y
                Render.screen.blit(s.image, (x, y))
        if flags & Render.TEXT:
            for t in Text.texts:
                x, y = t.parent.transform.pos.x, t.parent.transform.pos.y
                if 800 - Camera.pos.x > x > Camera.pos.x and 600 - Camera.pos.y > y > Camera.pos.y:
                    Render.screen.blit(t.font.render(t.text, True, (166, 127, 77)), (x - t.dx, y - t.dy - t.font_size * 0.16+2))
                    Render.screen.blit(t.font.render(t.text, True, t.color), (x - t.dx, y - t.dy - t.font_size * 0.16))
        if flags & Render.OVERLAY:
            for s in Render.shapes.values():
                points, color = s
                cpoints = []
                for p in points:
                    cpoints.append((p[0] + Camera.pos.x, p[1] + Camera.pos.y))
                pygame.draw.polygon(Render.screen, color, cpoints, width=2)
