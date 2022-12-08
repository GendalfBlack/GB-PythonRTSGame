from components import *


class Icon(UI):
    def __init__(self, pos=(0,0)):
        super().__init__(pos)


class TextUI(UI):
    def __init__(self, pos=(0,0)):
        super().__init__(pos)
        self.addComponent(Text(""))


class Button(UI):
    def __init__(self, pos=(0,0), text="Button"):
        super().__init__(pos)
        self.addComponent(Text(text))
        self.addComponent(OnClick())
