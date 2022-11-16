import pygame


class Component:
    def __init__(self, name):
        self.name = name
        self._parent = None


class ComponentsHolder:
    def __init__(self):
        self.components = {}
        self.pos = (0, 0)

    def addComponent(self, other):
        if isinstance(other, Component):
            self.components[other.name] = other
            other.parent = self


class GameObject(ComponentsHolder):
    def __init__(self):
        super().__init__()


class UI(ComponentsHolder):
    font = None
    font_size = 0

    def __init__(self):
        super().__init__()
        UI.font_size = 25
        UI.font = pygame.font.SysFont('Minecraft', UI.font_size)


class Background(ComponentsHolder):
    def __init__(self):
        super().__init__()


class SpriteLoader:
    sprites = {}

    def __init__(self):
        SpriteLoader.load("Sprites/tree-sprite.png", "tree")
        SpriteLoader.load("Sprites/house-sprite.png", "house")
        SpriteLoader.load("Sprites/grass-tile.png", "grass")

    @staticmethod
    def load(path, name):
        SpriteLoader.sprites[name] = pygame.image.load(path)


class Sprite(Component):
    sprites = []
    background = []
    ui = []

    def __init__(self, name, size):
        super().__init__("sprite")
        self.size = size
        self._sprite = SpriteLoader.sprites[name]
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

    def resize(self, size=None):
        if size:
            self.size = size
        self._sprite = pygame.transform.scale(self._sprite, self.size)

    def __lt__(self, other):
        return self.parent.pos[1] < other.parent.pos[1]


class Text(Component):
    texts = []

    def __init__(self, text, color=(0,0,0)):
        super().__init__("text")
        self._text = text
        self.color = color
        self.dx = 0
        self.dy = 0

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t
        self.dx = len(self._text)//2*UI.font_size*0.72
        self.dy = UI.font_size*0.16

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p
        Text.texts.append(self)


class Render:
    @staticmethod
    def render_sprites(screen):
        for s in Sprite.background:
            screen.blit(s.sprite, s.parent.pos)
        for s in Sprite.sprites:
            screen.blit(s.sprite, s.parent.pos)
        for s in Sprite.ui:
            screen.blit(s.sprite, s.parent.pos)
        for t in Text.texts:
            x, y = t.parent.pos[0], t.parent.pos[1]
            screen.blit(UI.font.render(t.text, True, t.color), (x-t.dx, y - t.dy))


class OnClick(Component):
    onClickEvents = []

    def __init__(self):
        super().__init__("onClick")
        self.function = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p

    def addEvent(self, other):
        self.function = other
        OnClick.onClickEvents.append(self)

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)
