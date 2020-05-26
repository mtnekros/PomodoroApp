import tkinter as tk
import utils

class AppCanvas(tk.Canvas):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

    def get_bounds(self, x, y, radius):
        x0 = x - radius
        y0 = y - radius
        x1 = x + radius
        y1 = y + radius
        return x0, y0, x1, y1

    def create_circle(self, x, y, radius, **kwargs):
        coords = self.get_bounds(x, y, radius)
        return self.create_oval(*coords, **kwargs)

    def create_circular_arc(self, x, y, radius, **kwargs):
        coords = self.get_bounds(x, y, radius)
        return self.create_arc(*coords, **kwargs)