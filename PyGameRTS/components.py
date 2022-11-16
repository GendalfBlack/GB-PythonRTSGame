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
    def __init__(self):
        super().__init__()


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
        self.layer = 0
        self.size = size
        self.sprite = SpriteLoader.sprites[name]
        self.resize(self.size)

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

    def resize(self, size):
        self.size = size
        self.sprite = pygame.transform.scale(self.sprite, size)

    def __lt__(self, other):
        return self.parent.pos[1] < other.parent.pos[1]


class Render:
    @staticmethod
    def render_sprites(screen):
        for s in Sprite.background:
            screen.blit(s.sprite, s.parent.pos)
        for s in Sprite.sprites:
            screen.blit(s.sprite, s.parent.pos)
        for s in Sprite.ui:
            screen.blit(s.sprite, s.parent.pos)


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
