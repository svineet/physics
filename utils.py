import math
import random
from kivy.utils import get_color_from_hex


def distance((x1, y1), (x2, y2)):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def random_color(alpha=1):
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
    c = random.choice(colors)
    c[-1] = alpha
    return c


def get_triangle_points(x, y, x2, y2):
    d = distance((x, y), (x2, y2))
    side = (2*d)/math.sqrt(5)
    hs = side/2

    return [x2-hs, y2, x2+hs, y2, x, y]


def constructTriangleFromLine(p1, p2):
    """
    Returns list of ordered pairs describing equilteral triangle around
    segment pt1 --> pt2.
    """
    halfHeightVector = (0.57735 * (p2[1] - p1[1]), 0.57735 * (p2[0] - p1[0]))
    p3 = (p1[0] + halfHeightVector[0], p1[1] - halfHeightVector[1])
    p4 = (p1[0] - halfHeightVector[0], p1[1] + halfHeightVector[1])
    return [p2[0], p2[1], p3[0], p3[1], p4[0], p4[1]]

def calc_center(points):
    """ Calculate the center of a polygon
    
        Return: The center (x,y)
    """
    tot_x, tot_y = 0,0
    for p in points:
        tot_x += p[0]
        tot_y += p[1]
    n = len(points)
    return (tot_x/n, tot_y/n)
