import pygame
from os import listdir
from os.path import isfile, join


class SpriteLoader:
    sprites = {}
    tiles = {}

    def __init__(self):
        SpriteLoader.load("Sprites/tree-sprite.png", "tree")
        SpriteLoader.load("Sprites/house-sprite.png", "house")
        SpriteLoader.load("Sprites/grass-tile.png", "grass")
        SpriteLoader.load("Sprites/black-color.png", "black")
        SpriteLoader.load("Sprites/ui-overlay.png", "ui")
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

