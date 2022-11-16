import pygame


class Component:
    def __init__(self, name):
        self.name = name


class ComponentsHolder:
    def __init__(self):
        self.components = {}
        self.pos = (0, 0)


class GameObject(ComponentsHolder):
    def __init__(self):
        super().__init__()



class UI(ComponentsHolder):
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


class SpriteComponent(Component):
    sprites = []

    def __init__(self, name, parent=None):
        super().__init__("sprite")
        if parent: self.parent = parent
        else: self.parent = None
        if issubclass(type(parent), UI): self.layer = 0
        else: self.layer = 1
        self.size = None
        self.sprite = SpriteLoader.sprites[name]
        SpriteComponent.sprites.append(self)
        SpriteComponent.sprites.sort()

    def resize(self, size):
        self.size = size
        self.sprite = pygame.transform.scale(self.sprite, size)

    def __lt__(self, other):
        if self.layer < other.layer: return False
        else: return self.parent.pos[1] < other.parent.pos[1]


class Render:
    @staticmethod
    def render_sprites(screen):
        for s in SpriteComponent.sprites:
            screen.blit(s.sprite, s.parent.pos)


class OnClickComponent(Component):
    components = []

    def __init__(self, parent=None):
        super().__init__("onClick")
        if parent:
            if isinstance(parent, GameObject): self.sprite = parent.components["sprite"].sprite
            elif isinstance(parent, UI): self.sprite = parent.sprite
            else: self.sprite = None
            self.parent = parent
        self.function = None

    def addEvent(self, other):
        self.function = other
        OnClickComponent.components.append(self)

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)
