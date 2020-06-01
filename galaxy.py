import math
import random
from aggdraw import Pen, Brush, Dib
from helpers import get_bounds, two_circles_overlap, get_random_pt_in, point_in_bounds

class SinFunction:
    def __init__(self, phase, del_theta, mean_value, amplitude):
        self.theta     = phase
        self.del_theta = del_theta
        self.amplitude = amplitude
        self.mean_value = mean_value

    @staticmethod
    def FromMinMaxValue(phase, del_theta, min_val, max_val):
        threshold = (min_val + max_val) / 2
        amplitude = (min_val - max_val) / 2
        return SinFunction( phase, del_theta, threshold, amplitude )

    def update(self):
        self.theta += self.del_theta

    def max_value(self):
        return self.amplitude + self.mean_value
        
    def __call__(self):
        return self.amplitude * math.sin(self.theta) + self.mean_value

class Star:
    IS_HEALTHY = "is healthy"
    IS_EXPLODING = "is exploding"
    IS_DEAD = "is dead"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.get_radius = SinFunction(
            phase=random.uniform(0,math.pi),
            amplitude=random.uniform(0.5,1.5),
            del_theta=random.uniform(0.03,0.07),
            mean_value=random.uniform(1.2,3.2)
        )
        self.status = Star.IS_HEALTHY
        self.radius = self.get_radius()
        self.color = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
        self.brush = Brush(self.color)
        self.pen = Pen(self.color,0)
        self.glow_brush = Brush(self.color, opacity=random.randint(20,40))
        self.glow_offset = self.get_radius.max_value() * 1.7
        self.explode_radius = self.get_radius.max_value() * 8

    def get_status(self):
        return self.status
    
    def update(self):
        if self.status == Star.IS_HEALTHY:
            self.get_radius.update()
            self.radius = self.get_radius()

        elif self.status == Star.IS_EXPLODING:
            self.radius += 0.3

            if self.radius > self.explode_radius:
                self.status = Star.IS_DEAD

    def explode(self):
        self.status = self.IS_EXPLODING

    def is_alive(self):
        return self.status != self.IS_DEAD

    def bounds(self, radius):
        x,y,r = self.x, self.y, radius
        return x-r, y-r, x+r ,y+r

    def draw(self, dib: Dib):
        if self.status == self.IS_HEALTHY:
            dib.ellipse( self.bounds(self.radius), self.pen, self.brush )
        dib.ellipse( self.bounds(self.radius + self.glow_offset), self.pen, self.glow_brush )

class DestructionCirle:
    def __init__(self):
        self.__is_growing = False
        self.__radius = 0
        self.__center = (0,0)
        self.__pen = Pen("red",0)
        self.__brush = Brush("red",50)

    @property
    def is_growing(self):
        return self.__is_growing

    def activate(self, x, y):
        self.__center = (x,y)
        self.__is_growing = True

    @property
    def bounds(self):
        return get_bounds(*self.__center, self.__radius)

    def grow(self, dr):
        self.__radius += dr
    
    def draw(self, drawer: Dib):
        if self.__is_growing:
            drawer.ellipse(self.bounds, self.__pen, self.__brush)

    def execute_destruction(self, galaxy):
        stars = galaxy.get_stars()
        kills = filter(lambda star: self.touches(star), stars)
        for kill in kills:
            kill.explode()
        self.reset()

    def update(self):
        if self.is_growing:
            self.__radius += 1

    def touches(self, star: Star):
        return two_circles_overlap(*self.__center, self.__radius, star.x, star.y, star.radius)
        
    def reset(self):
        self.__is_growing = False
        self.__radius = 0
        self.__center = (0,0)

class Galaxy:
    def __init__(self):
        self.stars = []
        self.birth_chance = 0.08
        self.death_chance = 0.02
        self.min_n_stars_for_death = 50
        self.max_n_stars = 300

    def birth_condition_is_met(self):
        return random.random() < self.birth_chance and len(self.stars) < self.max_n_stars

    def death_condition_is_met(self):
        return random.random() < self.death_chance and len(self.stars) > self.min_n_stars_for_death

    def update(self, spawn_bounds, restriction_bounds_list):
        if self.birth_condition_is_met():
            x,y = get_random_pt_in(spawn_bounds)
            if all([ not point_in_bounds(x, y, bounds ) for bounds in restriction_bounds_list ]):
                self.stars.append( Star( x,y ) )

        if self.death_condition_is_met():
            self.stars[0].explode()

        for star in self.stars:
            star.update()

        self.stars = list(filter(lambda star: star.is_alive(), self.stars))

    def draw(self, drawer):
        for star in self.stars:
            star.draw(drawer)

    def get_stars(self):
        return self.stars

    def explode_all_stars(self):
        for star in self.stars:
            star.explode()

    def reset(self):
        self.stars = []