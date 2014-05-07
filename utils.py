import math
import random
from kivy.utils import get_color_from_hex


def distance((x1, y1), (x2, y2)):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def random_color():
    colors = [
        "#33B5E5",
        "#0099CC",
        "#AA66CC",
        "#9933CC",
        "#99CC00",
        "#669900",
        "#FFBB33",
        "#FF8800",
        "#FF4444",
        "#CC0000"
    ]
    colors = [get_color_from_hex(x) for x in colors]
    return random.choice(colors)
