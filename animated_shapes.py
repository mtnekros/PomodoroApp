from aggdraw import Pen, Brush, Dib
from helpers import interpolate, get_bounds

class Ripple:
    def __init__(self, x, y, radius, min_radius, max_radius, min_width, max_width, color, growth_rate):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_width = min_width
        self.max_width = max_width
        self.growth_rate = growth_rate

    def calculate_width(self):
        assert( isinstance( self.radius,( float,int ) ) )
        return interpolate(
            self.max_width,
            self.min_width,
            self.min_radius,
            self.max_radius,
            self.radius
        )
    
    @property
    def bounds(self):
        return get_bounds(self.x, self.y, self.radius)

    def grow(self, dt):
        self.radius = self.radius + self.growth_rate * dt if self.radius < self.max_radius else self.min_radius
        self.width = self.calculate_width()

    def draw(self, dib: Dib):
        dib.eclipse(self.bounds, Pen(self.color, self.width))

    def translate(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

class ConcentricRipples:
    def __init__(self, x, y, min_radius, max_radius, color, nRipples):
        params = {
            "min_radius": min_radius,
            "max_radius": max_radius,
            "min_width": 1,
            "max_width": 6,
            "outline": color,
            "growth_rate": 30
        }
        self.ripples = []
        for iRipple in range(nRipples):
            radius = min_radius + iRipple * (max_radius - min_radius) / nRipples
            self.ripples.append( Ripple(x, y, radius, **params ) )

    def update(self, dt):
        for ripple in self.ripples:
            ripple.grow(dt)

    def translate(self, x, y):
        for ripple in self.ripples:
            ripple.translate(x, y)
        
    def draw(self, dib: Dib):
        for ripple in self.ripples:
            ripple.draw(dib)

class CountDownRing:
    MAX_EXTENT = 360
    def __init__(self, x, y, radius, width, color, shadow_color):
        self.x = x
        self.y = y
        self.radius = radius
        self.extent = CountDownRing.MAX_EXTENT
        self.pen = Pen(color, width=width)
        self.shadow_pen = Pen(shadow_color, width=width)

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