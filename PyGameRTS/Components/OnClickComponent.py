from Components.ComponentMaster import Component
from Components.BackgroundComponent import Background
from Components.GameObjectComponent import GameObject


class OnClick(Component):
    BG_LAYER = 0
    GO_LAYER = 0
    UI_LAYER = 0
    onClickEvents = []

    def __init__(self):
        super().__init__("onClick")
        self.function = None
        self.params = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p

    def addEvent(self, other, *params):
        self.function = other
        self.params = params
        if isinstance(self.parent, Background):
            OnClick.onClickEvents.insert(OnClick.BG_LAYER, self)
        elif isinstance(self.parent, GameObject):
            OnClick.onClickEvents.insert(OnClick.GO_LAYER, self)
            OnClick.BG_LAYER += 1
        else:
            OnClick.onClickEvents.insert(OnClick.UI_LAYER, self)
            OnClick.BG_LAYER += 1
            OnClick.GO_LAYER += 1

    def __call__(self):
        if len(self.params) == 0:
            self.function()
        else:
            self.function(self.params[0])

