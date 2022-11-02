from tkinter import *

w = Tk()

class Prog:
    c = None

    def __init__(self, w, width=800, height=600):
        Prog.c = Canvas(w, width=width, height=height)
        Prog.c.pack()


class Vector2:
    def __init__(self, x = None, y = None):
        if x:
            self.x = x
        else:
            self.x = 0
        if y:
            self.y = y
        else:
            self.y = 0

class Block:
    blocks = {}
    def __init__(self, **args):
        if "name" in args.keys():
            self.name = args["name"]
        if "text" in args.keys():
            self.text = args["text"]
        if "pos" in args.keys():
            self.pos = args["pos"]
        else:
            self.pos = Vector2()
        self.shape = None
        self.draw()
    def draw(self):
        Prog.c.create_text(self.pos.x, self.pos.y, text="?")
    def __add__(self, other):
        if self.point_out and other.point_in:
            Prog.c.create_line(
                self.point_out.x,
                self.point_out.y,
                other.point_in.x,
                other.point_in.y,
                arrow=LAST
                )


class Start(Block):
    def __init__(self, **args):
        super().__init__(name="start", text="start", **args)
        Block.blocks[self.name] = self
    def draw(self):
        self.width = 100
        self.height = 30
        self.shape = Prog.c.create_oval(
            self.pos.x-self.width/2,
            self.pos.y-self.height/2,
            self.pos.x+self.width/2,
            self.pos.y+self.height/2,
            fill="white")
        self.point_out = Vector2(self.pos.x,self.pos.y + self.height / 2)
        self.text = Prog.c.create_text(self.pos.x, self.pos.y, text=self.name)

class Finish(Block):
    def __init__(self, **args):
        super().__init__(name="finish", text="finish", **args)
        Block.blocks[self.name] = self
    def draw(self):
        self.width = 100
        self.height = 30
        self.shape = Prog.c.create_oval(
            self.pos.x - self.width / 2,
            self.pos.y - self.height / 2,
            self.pos.x + self.width / 2,
            self.pos.y + self.height / 2,
            fill="white")
        self.point_in = Vector2(self.pos.x,self.pos.y - self.height / 2)
        self.text = Prog.c.create_text(self.pos.x, self.pos.y, text=self.name)

Prog(w)
b1 = Start(pos=Vector2(100,100))
b2 = Finish(pos=Vector2(100,200))
b1+b2
w.mainloop()