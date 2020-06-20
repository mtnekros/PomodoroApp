import json
import requests
from datetime import datetime
import random

def quote_of_the_day():
    try:
        with open("quote-of-the-day.json", "r") as in_file:
            quote = json.loads(in_file.read())

        if quote["date"] != datetime.today().strftime("%Y-%m-%d"):
            response = requests.get("https://quotes.rest/qod?language=en")
            quote = response.json()["contents"]["quotes"][0]
            with open("quote-of-the-day.json", "w") as out_file:
                out_file.write(json.dumps(quote))
        
        return f"{quote['quote']}\n- {quote['author']}"
    except :
        return f"You can't always have quotes.\n- Pomodoro App"

def interpolate(x_min, x_max, y_min, y_max, y):
    return (x_max - x_min) / (y_max - y_min) * (y - y_min) + x_min

def get_bounds(center_x, center_y, radius):
    x,y,r = center_x, center_y, radius
    return x-r, y-r, x+r, y+r

def from_rgb(r :int, g :int, b :int):
    assert(all([v>=0 and v<=255 for v in (r,g,b)]))
    return "#" + hex(r<<16|g<<8|b).lstrip("0x")

def two_circles_overlap(x0, y0, r0, x1, y1, r1):
    distance_sq = (x1 - x0)**2 + (y1 - y0)**2
    return distance_sq <= (r0 + r1)**2

def assert_bound_is_valid(bounds):
    left,top,right,bottom = bounds
    assert left <= right, f"invalid bounds. left: {left} right: {right}"
    assert top <= bottom, f"invalid bounds. top: {top} bottom: {bottom}"

def point_in_bounds(x,y,bounds):
    assert_bound_is_valid( bounds )
    left,top,right,bottom = bounds
    return x >= left and x <= right and y >= top and y <= bottom

def get_random_pt_in(bounds):
    assert_bound_is_valid( bounds )
    left,top,right,bottom = bounds
    return random.uniform(left, right), random.uniform(top, bottom)

def widget_bounds(widget, offset):
    left, top = widget.winfo_x(), widget.winfo_y()
    return (
        left - offset,
        top - offset,
        left + widget.winfo_width() + offset,
        top + widget.winfo_height() + offset
    )