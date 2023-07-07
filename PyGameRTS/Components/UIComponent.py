from Components.ComponentsHolderComponent import ComponentsHolder
import pygame


class UI(ComponentsHolder):
    font = None
    font_size = 0

    def __init__(self, pos):
        super().__init__(pos)
        UI.font_size = 25
        UI.font = pygame.font.SysFont('Minecraft', UI.font_size)
