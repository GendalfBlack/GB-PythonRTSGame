from tkinter import *

w = Tk()

class Prog:
    c = None

    def __init__(self, w, width=800, height=600):
        Prog.c = Canvas(w, width=width, height=height)
        Prog.c.pack()


class Vector2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Block:
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

class Start(Block):
    def __init__(self, **args):
        super().__init__(name="start", text="start", **args)
    def draw(self):
        Prog.c.create_oval(self.pos.x-50, self.pos.y-15, self.pos.x+50, self.pos.y+15,fill="white")
        Prog.c.create_text(self.pos.x, self.pos.y, text=self.name)

class Finish(Block):
    def __init__(self, **args):
        super().__init__(name="finish", text="finish", **args)
    def draw(self):
        Prog.c.create_oval(self.pos.x-50, self.pos.y-15, self.pos.x+50, self.pos.y+15,fill="white")
        Prog.c.create_text(self.pos.x, self.pos.y, text=self.name)

Prog(w)
Start(pos=Vector2(100,100))
Finish(pos=Vector2(100,200))

w.mainloop()