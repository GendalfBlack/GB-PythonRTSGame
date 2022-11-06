from tkinter import *

w = Tk()

class Prog:
    c = None

    def __init__(self, w, width=800, height=600):
        Prog.c = Canvas(w, width=width, height=height)
        Prog.c.pack()


class Vector2:
    def __init__(self, x = None, y = None, side = None):
        if x:
            self.x = x
        else:
            self.x = 0
        if y:
            self.y = y
        else:
            self.y = 0
        if side:
            self.side=side
        else:
            self.side="down"

class Block:
    blocks = {}
    def __init__(self, **args):
        if "value" in args.keys():
            self.action = args["value"]
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
            if self.point_out.x == other.point_in.x:
                Prog.c.create_line(self.point_out.x, self.point_out.y, other.point_in.x, other.point_in.y, arrow=LAST)
            elif self.point_out.side == "left" or self.point_out.side == "right":
                Prog.c.create_line(self.point_out.x, self.point_out.y, other.point_in.x, self.point_out.y)
                Prog.c.create_line(other.point_in.x, self.point_out.y, other.point_in.x, other.point_in.y, arrow=LAST)
            elif self.point_out.x < other.point_in.x and self.point_out.side == "down":
                Prog.c.create_line(self.point_out.x, self.point_out.y, self.point_out.x, self.point_out.y+(other.point_in.y-self.point_out.y)/2)
                Prog.c.create_line(self.point_out.x, self.point_out.y+(other.point_in.y-self.point_out.y)/2, other.point_in.x, self.point_out.y+(other.point_in.y-self.point_out.y)/2)
                Prog.c.create_line(other.point_in.x, self.point_out.y+(other.point_in.y-self.point_out.y)/2, other.point_in.x, other.point_in.y, arrow=LAST)
            try:
                if self.point_out2:
                    self.point_out = self.point_out2
            except:
                pass

class Computation(Block):
    counter = 0
    def __init__(self, **args):
        super().__init__(name="computation", text="start", **args)
        Block.blocks[f"{self.name}{Computation.counter}"] = self
    def draw(self):
        self.width=100
        self.height=30
        self.shape = Prog.c.create_rectangle(
            self.pos.x - self.width/2,
            self.pos.y - self.height/2,
            self.pos.x + self.width/2,
            self.pos.y + self.height/2,
            fill="white")
        self.point_in = Vector2(self.pos.x, self.pos.y - self.height / 2)
        self.point_out = Vector2(self.pos.x,self.pos.y + self.height / 2)
        self.text = Prog.c.create_text(self.pos.x,self.pos.y,text=self.action)

class Condition(Block):
    counter = 0
    def __init__(self, **args):
        super().__init__(name="computation", text="start", **args)
        Block.blocks[f"{self.name}{Computation.counter}"] = self
    def draw(self):
        self.width=100
        self.height=30
        points =(
            self.pos.x, self.pos.y - self.height/2,
            self.pos.x - self.width/2, self.pos.y,
            self.pos.x, self.pos.y + self.height/2,
            self.pos.x + self.width / 2, self.pos.y,
        )
        self.shape = Prog.c.create_polygon(points, fill="white",outline="black")
        self.point_in = Vector2(self.pos.x, self.pos.y - self.height / 2)
        self.point_out = Vector2(self.pos.x - self.width / 2, self.pos.y, "right")
        self.point_out2 = Vector2(self.pos.x + self.width / 2, self.pos.y, "left")
        self.text = Prog.c.create_text(self.pos.x,self.pos.y,text=self.action)
        self.out_text = Prog.c.create_text(self.point_out.x,self.point_out.y-12, text="True")
        self.out_text = Prog.c.create_text(self.point_out2.x, self.point_out2.y - 12, text="False")

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
b1 = Start(pos=Vector2(250,100))
b2 = Condition(pos=Vector2(300,200), value="i<0")
b3 = Computation(pos=Vector2(150,250), value="i=0")
b4 = Computation(pos=Vector2(150,350), value="i+=1")
b5 = Finish(pos=Vector2(450,250))
b1+b2
b2+b3
b2+b5
b3+b4
w.mainloop()