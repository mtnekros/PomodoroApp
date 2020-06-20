from aggdraw import Pen, Dib
from utils import get_bounds, interpolate


class CountDownRing:
    MAX_EXTENT = 360
    def __init__(self, x, y, radius, width, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.extent = CountDownRing.MAX_EXTENT
        self.pen = Pen(color, width=width, opacity=190)
        self.shadow_pen = Pen(color, width=width, opacity=60)

    @property
    def bounds(self):
        return get_bounds(self.x, self.y, self.radius)

    def update(self, time_left, duration):
        self.extent = interpolate(0, CountDownRing.MAX_EXTENT, 0, duration, time_left)

    def reset(self):
        self.extent = CountDownRing.MAX_EXTENT

    def translate(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
    def draw(self, dib: Dib):
        dib.arc(self.bounds, 90, CountDownRing.MAX_EXTENT + 90, self.shadow_pen)
        dib.arc(self.bounds, CountDownRing.MAX_EXTENT+90-self.extent, 90, self.pen)