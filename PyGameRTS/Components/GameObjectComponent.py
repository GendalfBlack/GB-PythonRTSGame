from Components.ComponentsHolderComponent import ComponentsHolder


class GameObject(ComponentsHolder):
    def __init__(self, pos):
        super().__init__(pos)
