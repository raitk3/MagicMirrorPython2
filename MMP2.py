import pygame as pg
from custom_modules.bus_times import BusTimes
from pages import Page
from size import Size
from custom_modules.time_keeper import TimeKeeper

font_name = "Consolas"

class MagicMirror:
    def __init__(self):
        pg.init()
        self.state = Page.BUS_TIME
        self.window_size = (800, 480)
        self.screen = pg.display.set_mode(self.window_size, pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.running = True
        self.main_modules = [TimeKeeper(self, 0, 0)]
        self.states = {
            Page.BUS_TIME: [BusTimes(self, 0, 200, 2), BusTimes(self, 400, 200, 3)]
        }
        self.fonts = self.generate_fonts()


    def generate_fonts(self):
        fonts = {}
        for el in Size.list():
            fonts[el] = pg.font.SysFont(font_name, el)
        return fonts

    def get_font(self, size: Size):
        int_to_find = size.value
        return self.fonts[int_to_find]

    def event(self):
        event_list = pg.event.get()
        for event in event_list:
            if event.type == pg.QUIT:
                pg.quit()

    def update(self):
        for el in self.main_modules:
            el.update()
        if self.state in self.states:
            for el in self.states[self.state]:
                el.update()


    def render(self):
        for el in self.main_modules:
            el.render()
        if self.state in self.states:
            for el in self.states[self.state]:
                el.render()
        pg.display.update()

    def run(self):
        while self.running:
            self.event()
            self.update()
            self.screen.fill(("black"))
            self.render()
            self.clock.tick(1)

if __name__ == '__main__':
    mm = MagicMirror()
    mm.run()
    pg.quit()