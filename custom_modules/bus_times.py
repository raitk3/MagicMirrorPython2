import imp
import pygame as pg
from size import Size
from datetime import datetime
import requests

list_of_stops = [
    ("881", "Keemia", False),
    ("888", "Tehnikaülikool", False),
    ("1414", "Punane", False),
    ("1446", "Punane", False),
    ("25469", "Risti (-> Haapsalu)", False),
    ("25470", "Risti (-> Tallinn)", False)
]

class BusTimes():
    def __init__(self, root,  x, y, stop):
        self.root = root
        self.x, self.y = x, y
        self.last_updated = None
        self.stop = list_of_stops[stop]
        self.schedule = []

    def get_mock_bus_times(self, force_update):
        if self.stop == ("1414", "Punane", False):
            return [["31", "Estonia", 10, "trol"], ["31", "Priisle", 699, "trol"], ["13", "Seli", 12414, "bus"]]
        return [["13", "Väike-Õismäe", 300, "bus"], ["50", "Majaka põik", 500, "bus"], ["7", "Sõjamäe", 600, "trol"]]

    def get_now_in_seconds(self):
        now = datetime.now().strftime("%H:%M:%S")
        elements = [int(el) for el in now.split(":")]
        return elements[0] * 3600 + elements[1] * 60 + elements[2]
    
    def get_bus_times(self, force_update):
        time_right_now = self.get_now_in_seconds()
        if \
                force_update \
                or len(self.schedule) < 3 \
                or self.schedule[0][2] < time_right_now \
                or self.last_updated == None \
                or time_right_now - self.last_updated > 300:
            list_of_buses = []
            response = requests.get(
                f"https://transport.tallinn.ee/siri-stop-departures.php?stopid={self.stop[0]}&time=0"
            )
            rows = response.text.split("\n")[2:-1]
            for i, row in enumerate(rows):
                if i < 3:
                    data = row.split(",")
                    bus_trol = data[0]
                    line_number = data[1]
                    eta = int(data[2])
                    terminus = data[4]
                    list_of_buses.append(
                        [line_number, terminus, eta, bus_trol])
                else:
                    break
            self.last_updated = time_right_now
            return list_of_buses
        return self.schedule

    def get_time_remaining_string(self, scheduled_time):
        
        time_remaining = ((scheduled_time - self.get_now_in_seconds()) % (24 * 60 * 60))
        hours = time_remaining // 3600
        minutes = (time_remaining // 60) % 60
        if minutes == 0 and hours > 0:
            return f"{hours} tunni pärast."
        if minutes < 1:
            return "Vähem kui 1 minuti pärast"
        if hours > 0:
            return f"{hours} tunni ja {minutes} minuti pärast"
        return f"{minutes} minuti pärast"

    def update(self):
        self.schedule = self.get_bus_times(False)

    def render(self):
        print(self.schedule)
        row_gap = 100
        col_cap = 100
        
        for i, el in enumerate(self.schedule):
            color = "#56C1A6" if el[3] == "bus" else "#3466B1"
            pg.draw.rect(self.root.screen, color, pg.Rect(self.x, self.y + row_gap * i, 80, 80),  4, 12, 12, 12, 12)
            number = self.root.get_font(Size.LARGE).render(str(el[0]), True, "#FFFFFF")
            x, y = number.get_size()
            self.root.screen.blit(number, (self.x - x//2 + 40, self.y - y//2 + 35 + row_gap * i + 8))
            terminus = self.root.get_font(Size.X_SMALL).render(el[1], True, "#FFFFFF")
            self.root.screen.blit(terminus, (self.x + col_cap, self.y + row_gap * i))
            time_remaining = self.root.get_font(Size.XXX_SMALL).render(self.get_time_remaining_string(el[2]), True, "#888888")
            self.root.screen.blit(time_remaining, (self.x + col_cap, self.y + 45 + row_gap * i))