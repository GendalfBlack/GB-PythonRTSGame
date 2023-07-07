import pygame
from Components.ComponentMaster import Component


class Transform(Component):
    def __init__(self, pos=(0, 0)):
        super().__init__("transform")
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.size = pygame.Vector2()

