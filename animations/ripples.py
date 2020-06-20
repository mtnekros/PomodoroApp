from aggdraw import Pen, Brush, Dib
from utils import interpolate, get_bounds

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
            "color": color,
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