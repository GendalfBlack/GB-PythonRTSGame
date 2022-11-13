import pygame
from gameClass import Game

class SpriteLoader:
    sprites = {}
    def __init__(self):
        self.load("Sprites/tree-sprite.png", "tree")
        self.load("Sprites/house-sprite.png", "house")
        self.load("Sprites/grass-tile.png", "grass")
    def load(self, path, name):
        SpriteLoader.sprites[name] = pygame.image.load(path)

class GameObject:
    def __init__(self, pos = None, **args):
        self.pos = pos
        if "name" in args.keys():
            self.name = args["name"]
        else:
            self.name = "Empty"
        if "sprite" in args.keys():
            self.sprite = SpriteLoader.sprites[args["sprite"]]
        else:
            self.sprite = None
        if "size" in args.keys():
            self.size = args["size"]
            self.sprite = pygame.transform.scale(self.sprite, args["size"])
        else:
            self.size = (0,0)
        self.instantiate()
    def instantiate(self):
        if self not in Game.gameobjects:
            Game.gameobjects.append(self)
    def draw(self):
        Game.screen.blit(self.sprite, self.pos)