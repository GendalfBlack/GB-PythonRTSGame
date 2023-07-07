from Components.UIComponent import UI
from Components.ComponentMaster import Component
import pygame

class Text(Component):
    TOP = 1
    LEFT = 2
    CENTER = 4
    texts = []

    def __init__(self, text, color=(0, 0, 0), font_size=25, flags=CENTER):
        super().__init__("text")
        self._text = text
        self.color = color
        self.dx = 0
        self.dy = 0
        self.font_size = font_size
        self.font = pygame.font.SysFont('Minecraft', font_size)
        self.flags = flags

    def set_font_size(self, font_size):
        self.font_size = font_size
        self.font = pygame.font.SysFont('Minecraft', font_size)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t
        if self.flags == Text.CENTER:
            self.dx = len(self._text) // 2 * UI.font_size * 0.72
            self.dy = UI.font_size * 0.16

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p
        w, h = UI.font_size * 0.67 * len(self._text), UI.font_size * 0.89
        p.transform.size = pygame.Vector2(w, h)
        Text.texts.append(self)
