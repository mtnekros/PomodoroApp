from helpers import interpolate

class Ripple:
    def __init__(self, canvas, x, y, radius, min_radius, max_radius, min_width, max_width, outline, growth_rate):
        self.x = x
        self.y = y
        self.radius = radius
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_width = min_width
        self.max_width = max_width
        self.canvas = canvas
        self.growth_rate = growth_rate
        self.id = self.canvas.create_circle(x, y, radius, width=self.get_width(), outline=outline)

    def get_width(self):
        assert( isinstance( self.radius,( float,int ) ) )
        return interpolate(
            self.max_width,
            self.min_width,
            self.min_radius,
            self.max_radius,
            self.radius
        )

    def grow(self, dt):
        self.radius = self.radius + self.growth_rate * dt if self.radius < self.max_radius else self.min_radius
        self.canvas.coords(self.id, self.canvas.get_bounds(self.x, self.y, self.radius))
        self.canvas.itemconfig(self.id, width=self.get_width())

    def set_visible(self, visible):
        state = "normal" if visible else "hidden"
        self.canvas.itemconfig(self.id, state=state)

    def translate(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

class Ripples:
    def __init__(self, canvas, x, y, min_radius, max_radius, color, nRipples):
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
            self.ripples.append( Ripple(canvas, x, y, radius, **params ) )

    def update(self, dt):
        for ripple in self.ripples:
            ripple.grow(dt)

    def set_visible(self, visible):
        for ripple in self.ripples:
            ripple.set_visible(visible)

    def translate(self, x, y):
        for ripple in self.ripples:
            ripple.translate(x, y)

class CountDownRing:
    MAX_EXTENT = 359.99
    def __init__(self, canvas, x, y, radius, width, outline):
        self.x = x
        self.y = y
        self.radius = radius
        self.canvas = canvas
        self.id = canvas.create_circular_arc(x, y, radius, start=90, extent=359.99, style="arc", width=width, outline=outline)

    def update(self, time_left, duration):
        self.canvas.itemconfig(self.id, extent=interpolate(0, CountDownRing.MAX_EXTENT, 0, duration, time_left))

    def reset(self):
        self.canvas.itemconfig(self.id, extent=CountDownRing.MAX_EXTENT)

    def translate(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.canvas.coords(self.id, self.canvas.get_bounds(self.x, self.y, self.radius))