import locale
import pygame as pg
from datetime import datetime
from size import Size

class TimeKeeper():
    def __init__(self, root,  x, y):
        self.root = root
        self.x, self.y = x, y
        self.date = "xx. yyyyyyyyy"
        self.time = "HH:MM"

    def update(self):
        self.time = datetime.now().strftime("%H:%M")
        self.date = datetime.now().strftime("%A, %d. %B")

    def render(self):
        d = self.root.get_font(Size.SMALL).render(self.date, True, "white")
        self.root.screen.blit(d, (self.x, self.y))
        t = self.root.get_font(Size.XXX_LARGE).render(self.time, True, "white")
        self.root.screen.blit(t, (self.x, self.y + Size.SMALL.value * 5/8))
