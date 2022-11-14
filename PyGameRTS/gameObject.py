import pygame
from gameClass import Game
from spriteComponent import SpriteComponent


class GameObject:
    clicked = None

    def __init__(self, pos = None, **args):
        self.pos = pos
        if "name" in args.keys(): self.name = args["name"]
        else: self.name = "Empty"
        if "sprite" in args.keys(): self.sprite = SpriteComponent(args["sprite"], self)
        else: self.sprite = None
        if "size" in args.keys():
            self.size = args["size"]
            self.sprite.resize(self.size)
        else: self.size = (0,0)

