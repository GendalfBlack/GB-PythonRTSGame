import pygame
from os import listdir
from os.path import isfile, join


class Component:
    def __init__(self, name):
        self.name = name
        self._parent = None


class ComponentsHolder:
    def __init__(self, pos=(0, 0)):
        self.components = {}
        self.transform = Transform(pos)
        self.addComponent(self.transform)

    def addComponent(self, other):
        if isinstance(other, Component):
            self.components[other.name] = other
            other.parent = self


class GameObject(ComponentsHolder):
    def __init__(self, pos):
        super().__init__(pos)


class UI(ComponentsHolder):
    font = None
    font_size = 0

    def __init__(self, pos):
        super().__init__(pos)
        UI.font_size = 25
        UI.font = pygame.font.SysFont('Minecraft', UI.font_size)


class Background(ComponentsHolder):
    def __init__(self, pos):
        super().__init__(pos)


class SpriteLoader:
    sprites = {}
    tiles = {}

    def __init__(self):
        SpriteLoader.load("Sprites/tree-sprite.png", "tree")
        SpriteLoader.load("Sprites/house-sprite.png", "house")
        SpriteLoader.load("Sprites/grass-tile.png", "grass")
        SpriteLoader.load("Sprites/black-color.png", "black")
        path = "D:/2.3.PythonPublic/GB-PythonProjects/PyGameRTS/Hand-drawn-sprites"
        tiles = [f for f in listdir(path) if isfile(join(path,f))]
        for t in tiles:
            SpriteLoader.loadTile("Hand-drawn-sprites/"+t, t.split('.')[0])

    @staticmethod
    def load(path, name):
        SpriteLoader.sprites[name] = pygame.image.load(path)

    @staticmethod
    def loadTile(path, name):
        SpriteLoader.tiles[name] = pygame.image.load(path)


class Transform(Component):
    def __init__(self, pos=(0, 0)):
        super().__init__("transform")
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.size = pygame.Vector2()


class Sprite(Component):
    sprites = []
    background = []
    ui = []

    def __init__(self, name, size):
        super().__init__("sprite")
        if type(size) is tuple:
            self.size = pygame.Vector2(size[0], size[1])
        else:
            self.size = pygame.Vector2()
        if name in SpriteLoader.sprites.keys():
            self._sprite = SpriteLoader.sprites[name]
        else:
            self._sprite = SpriteLoader.tiles[name]
        self.sprite_name = name
        if name.count("_") > 0:
            self.sides = name.split("_")
        self.resize(self.size)

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, s):
        self._sprite = s
        self.resize()

    def swap(self, s):
        self.sprite = s

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p
        if isinstance(p, Background):
            Sprite.background.append(self)
            Sprite.background.sort()
        elif isinstance(p, UI):
            Sprite.ui.append(self)
            Sprite.ui.sort()
        else:
            Sprite.sprites.append(self)
            Sprite.sprites.sort()
        p.transform.size = self.size

    def resize(self, size=None):
        if size:
            self.size = size
        self._sprite = pygame.transform.scale(self._sprite, self.size)

    def __lt__(self, other):
        return self.parent.transform.pos.y < other.parent.transform.pos.y


class Text(Component):
    TOP = 1
    LEFT = 2
    CENTER = 4
    texts = []

    def __init__(self, text, color=(0, 0, 0), flags=CENTER):
        super().__init__("text")
        self._text = text
        self.color = color
        self.dx = 0
        self.dy = 0
        self.flags = flags

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t
        if self.flags == Text.CENTER:
            self.dx = len(self._text) // 2 * UI.font_size * 0.72
            self.dy = UI.font_size * 0.16

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p
        w, h = UI.font_size * 0.67 * len(self._text), UI.font_size * 0.89
        p.transform.size = pygame.Vector2(w, h)
        Text.texts.append(self)


class Camera:
    pos = pygame.Vector2(-50,-75)
    cord = (-50,-75)


class Render:
    NONE = 1
    BACKGROUND = 2
    SPRITE = 4
    UI = 8
    TEXT = 16
    OVERLAY = 32
    ALL = 63

    screen = None
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
        if flags & Render.BACKGROUND:
            for s in Sprite.background:
                x, y = s.parent.transform.pos.x, s.parent.transform.pos.y
                Render.screen.blit(s.sprite, (x + Camera.pos.x, y + Camera.pos.y))
        if flags & Render.SPRITE:
            for s in Sprite.sprites:
                x, y = s.parent.transform.pos.x, s.parent.transform.pos.y
                Render.screen.blit(s.sprite, (x + Camera.pos.x, y + Camera.pos.y))
        if flags & Render.UI:
            for s in Sprite.ui:
                x, y = s.parent.transform.pos.x, s.parent.transform.pos.y
                Render.screen.blit(s.sprite, (x, y))
        if flags & Render.TEXT:
            for t in Text.texts:
                x, y = t.parent.transform.pos.x, t.parent.transform.pos.y
                Render.screen.blit(UI.font.render(t.text, True, t.color), (x - t.dx, y - t.dy - UI.font_size * 0.16))
        if flags & Render.OVERLAY:
            for s in Render.shapes.values():
                points, color = s
                cpoints = []
                for p in points:
                    cpoints.append((p[0] + Camera.pos.x, p[1] + Camera.pos.y))
                pygame.draw.polygon(Render.screen, color, cpoints, width=2)


class OnClick(Component):
    BG_LAYER = 0
    GO_LAYER = 0
    UI_LAYER = 0
    onClickEvents = []

    def __init__(self):
        super().__init__("onClick")
        self.function = None
        self.params = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p

    def addEvent(self, other, *params):
        self.function = other
        self.params = params
        if isinstance(self.parent, Background):
            OnClick.onClickEvents.insert(OnClick.BG_LAYER, self)
        elif isinstance(self.parent, GameObject):
            OnClick.onClickEvents.insert(OnClick.GO_LAYER, self)
            OnClick.BG_LAYER += 1
        else:
            OnClick.onClickEvents.insert(OnClick.UI_LAYER, self)
            OnClick.BG_LAYER += 1
            OnClick.GO_LAYER += 1

    def __call__(self):
        self.function(self.params[0])


class Collider2D(Component):
    colliders = []

    def __init__(self):
        super().__init__("collider2D")
        Collider2D.colliders.append(self)
        self.custom = False
        self._points = []

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p
        sx, sy = p.transform.pos.x, p.transform.pos.y
        sw, sh = p.transform.size.x, p.transform.size.y
        self._points.append(pygame.Vector2(sx, sy))
        self._points.append(pygame.Vector2(sx + sw, sy))
        self._points.append(pygame.Vector2(sx + sw, sy + sh))
        self._points.append(pygame.Vector2(sx, sy + sh))

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, pts):
        self._points = []
        sx, sy = self.parent.transform.pos.x, self.parent.transform.pos.y
        self._points.append(pygame.Vector2(sx + pts[0][0], sy + pts[0][1]))
        self._points.append(pygame.Vector2(sx + pts[1][0], sy + pts[1][1]))
        self._points.append(pygame.Vector2(sx + pts[2][0], sy + pts[2][1]))
        self._points.append(pygame.Vector2(sx + pts[3][0], sy + pts[3][1]))
        self.custom = True

    def draw_hit_box(self, screen):
        if not isinstance(self.parent, UI):
            pts = []
            for p in self._points:
                pts.append(p + Camera.pos)
        else:
            pts = self._points
        pygame.draw.polygon(screen, (255, 0, 0), pts, 2)

    def collide_point(self, x, y):
        dx = 0
        dy = 0
        if not isinstance(self.parent, UI):
            dx = Camera.pos.x
            dy = Camera.pos.y
        if not self.custom:
            sx, sy = self._points[0][0] + dx, \
                     self._points[0][1] + dy
            sw = self._points[1][0] - self._points[0][0]
            sh = self._points[2][1] - self._points[1][1]
            if pygame.Rect(sx, sy, sw, sh).collidepoint(x, y):
                return True
            else:
                return False
        else:
            x0, x1 = self._points[0][0] + dx, self._points[1][0] + dx
            y0, y1 = self._points[0][1] + dy, self._points[1][1] + dy
            x2, x3 = self._points[2][0] + dx, self._points[3][0] + dx
            y2, y3 = self._points[2][1] + dy, self._points[3][1] + dy
            a1 = (y1 - y0) / (x1 - x0)
            b1 = y0 - a1 * x0
            a2 = (y2 - y1) / (x2 - x1)
            b2 = y1 - a2 * x1
            a3 = (y3 - y2) / (x3 - x2)
            b3 = y2 - a3 * x2
            a4 = (y0 - y3) / (x0 - x3)
            b4 = y3 - a4 * x3
            if a1 * x + b1 < y < a3 * x + b3 and a2 * x + b2 < y < a4 * x + b4:
                return True
            else:
                return False
