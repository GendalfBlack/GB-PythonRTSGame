from Components.ComponentMaster import Component
from Components.UIComponent import UI
from Components.CameraComponent import Camera
import pygame


class Collider2D(Component):
    colliders = []

    def __init__(self):
        super().__init__("collider2D")
        Collider2D.colliders.append(self)
        self.custom = False
        self._points = []

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p
        sx, sy = p.transform.pos.x, p.transform.pos.y
        sw, sh = p.transform.size.x, p.transform.size.y
        self._points.append(pygame.Vector2(sx, sy))
        self._points.append(pygame.Vector2(sx + sw, sy))
        self._points.append(pygame.Vector2(sx + sw, sy + sh))
        self._points.append(pygame.Vector2(sx, sy + sh))

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, pts):
        self._points = []
        sx, sy = self.parent.transform.pos.x, self.parent.transform.pos.y
        self._points.append(pygame.Vector2(sx + pts[0][0], sy + pts[0][1]))
        self._points.append(pygame.Vector2(sx + pts[1][0], sy + pts[1][1]))
        self._points.append(pygame.Vector2(sx + pts[2][0], sy + pts[2][1]))
        self._points.append(pygame.Vector2(sx + pts[3][0], sy + pts[3][1]))
        self.custom = True

    def draw_hit_box(self, screen):
        if not isinstance(self.parent, UI):
            pts = []
            for p in self._points:
                pts.append(p + Camera.pos)
        else:
            pts = self._points
        pygame.draw.polygon(screen, (255, 0, 0), pts, 2)

    def collide_point(self, x, y):
        dx = 0
        dy = 0
        if not isinstance(self.parent, UI):
            dx = Camera.pos.x
            dy = Camera.pos.y
        if not self.custom:
            sx, sy = self._points[0][0] + dx, \
                     self._points[0][1] + dy
            sw = self._points[1][0] - self._points[0][0]
            sh = self._points[2][1] - self._points[1][1]
            if pygame.Rect(sx, sy, sw, sh).collidepoint(x, y):
                return True
            else:
                return False
        else:
            x0, x1 = self._points[0][0] + dx, self._points[1][0] + dx
            y0, y1 = self._points[0][1] + dy, self._points[1][1] + dy
            x2, x3 = self._points[2][0] + dx, self._points[3][0] + dx
            y2, y3 = self._points[2][1] + dy, self._points[3][1] + dy
            a1 = (y1 - y0) / (x1 - x0)
            b1 = y0 - a1 * x0
            a2 = (y2 - y1) / (x2 - x1)
            b2 = y1 - a2 * x1
            a3 = (y3 - y2) / (x3 - x2)
            b3 = y2 - a3 * x2
            a4 = (y0 - y3) / (x0 - x3)
            b4 = y3 - a4 * x3
            if a1 * x + b1 < y < a3 * x + b3 and a2 * x + b2 < y < a4 * x + b4:
                return True
            else:
                return False