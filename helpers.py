def interpolate(x_min, x_max, y_min, y_max, y):
    return (x_max - x_min) / (y_max - y_min) * (y - y_min) + x_min