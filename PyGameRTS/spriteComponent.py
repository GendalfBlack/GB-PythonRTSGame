import pygame


class UI:
    pass


class SpriteLoader:
    sprites = {}

    def __init__(self):
        SpriteLoader.load("Sprites/tree-sprite.png", "tree")
        SpriteLoader.load("Sprites/house-sprite.png", "house")
        SpriteLoader.load("Sprites/grass-tile.png", "grass")

    @staticmethod
    def load(path, name):
        SpriteLoader.sprites[name] = pygame.image.load(path)


class SpriteComponent:
    sprites = []

    def __init__(self, name, parent = None):
        if parent: self.parent = parent
        else: self.parent = None
        if issubclass(type(parent), UI): self.layer = 0
        else: self.layer = 1

        self.sprite = SpriteLoader.sprites[name]
        SpriteComponent.sprites.append(self)
        SpriteComponent.sprites.sort()

    def resize(self, size):
        self.sprite = pygame.transform.scale(self.sprite, size)

    def __lt__(self, other):
        if self.layer < other.layer: return False
        else: return self.parent.pos[1] < other.parent.pos[1]


class Render:
    @staticmethod
    def render_sprites(screen):
        for s in SpriteComponent.sprites:
            screen.blit(s.sprite, s.parent.pos)