from Components.ComponentMaster import Component
from Components.SpriteLoaderComponent import SpriteLoader
from Components.BackgroundComponent import Background
from Components.UIComponent import UI
import pygame


class Sprite(pygame.sprite.Sprite, Component):
    ui_sprites = pygame.sprite.LayeredUpdates()
    background_sprites = pygame.sprite.LayeredUpdates()
    game_sprites = pygame.sprite.LayeredUpdates()
    all_sprites = pygame.sprite.LayeredUpdates()

    def __init__(self, name, size):
        super().__init__(self.all_sprites)
        Component.__init__(self, "sprite")
        self.size = pygame.Vector2(size[0], size[1]) if isinstance(size, tuple) else pygame.Vector2()
        if name in SpriteLoader.sprites.keys():
            self.image = pygame.transform.scale(SpriteLoader.sprites[name], self.size)
        else:
            self.image = pygame.transform.scale(SpriteLoader.tiles[name], self.size)
        self.rect = self.image.get_rect()
        self.rect.size = self.size
        self.sprite_name = name
        if name.count("_") > 0:
            self.sides = name.split("_")
        self.resize(self.size)

    @property
    def parent(self):
        return self._parent

    def swap(self, s):
        self.image = pygame.transform.scale(s, self.size)

    @parent.setter
    def parent(self, p):
        self._parent = p
        if isinstance(p, Background):
            Sprite.background_sprites.add(self, layer=0)
        elif isinstance(p, UI):
            self.rect.x = p.transform.pos.x
            self.rect.y = p.transform.pos.y
            Sprite.ui_sprites.add(self, layer=2)
        else:
            Sprite.game_sprites.add(self, layer=1)
        p.transform.size = self.size

    def resize(self, size=None):
        if size:
            self.size = size
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect.size = self.size

