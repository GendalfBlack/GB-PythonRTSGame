from spriteComponent import SpriteLoader, SpriteComponent, UI


class UIIcon(UI):
    def __init__(self, pos = None, **args):
        self.ui = True
        if pos: self.pos = pos
        else: self.pos = (0,0)
        if "sprite" in args.keys(): self.sprite = SpriteComponent(args["sprite"], self)
        else: self.sprite = None
        if "size" in args.keys():
            self.size = args["size"]
            self.sprite.resize(self.size)
        else: self.size = (0,0)