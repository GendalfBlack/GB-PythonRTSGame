class SpriteLoader:
    sprites = {}
    def __init__(self):
        self.load("Sprites/tree-sprite.png", "tree")
        self.load("Sprites/house-sprite.png", "house")
    def load(self, path, name):
        sprites[name] = image.load(path)

class GameObject:
    def __init__(self, pos = None, **args):
        self.pos = pos
        self.sprite = None
        if "name" in args.keys():
            self.name = args["name"]
        else:
            self.name = "Empty"