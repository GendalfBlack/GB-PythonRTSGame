import pygame


class Component:
    def __init__(self, name):
        self.name = name
        self._parent = None


class ComponentsHolder:
    def __init__(self, pos=(0,0)):
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

    def __init__(self):
        SpriteLoader.load("Sprites/tree-sprite.png", "tree")
        SpriteLoader.load("Sprites/house-sprite.png", "house")
        SpriteLoader.load("Sprites/grass-tile.png", "grass")

    @staticmethod
    def load(path, name):
        SpriteLoader.sprites[name] = pygame.image.load(path)


class Transform(Component):
    def __init__(self, pos=(0,0)):
        super().__init__("transform")
        self.pos = pygame.Vector2(pos[0],pos[1])


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
        return self.parent.transform.pos.y < other.parent.transform.pos.y


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


class Camera:
    pos = pygame.Vector2()


class Render:
    @staticmethod
    def render_sprites(screen):
        for s in Sprite.background:
            x, y = s.parent.transform.pos.x, s.parent.transform.pos.y
            screen.blit(s.sprite, (x + Camera.pos.x, y + Camera.pos.y))
        for s in Sprite.sprites:
            x, y = s.parent.transform.pos.x, s.parent.transform.pos.y
            screen.blit(s.sprite, (x + Camera.pos.x, y + Camera.pos.y))
        for s in Sprite.ui:
            x, y = s.parent.transform.pos.x, s.parent.transform.pos.y
            screen.blit(s.sprite, (x, y))
        for t in Text.texts:
            x, y = t.parent.transform.pos.x, t.parent.transform.pos.y
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
