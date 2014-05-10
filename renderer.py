import math
import cymunk
from kivy.graphics import Color, Ellipse, Rectangle, Rotate, Line
from kivy.properties import DictProperty, ListProperty

from utils import random_color as get_rand_color

FRICTION = 0.5
PIN_RADIUS = 5
from tools import LINE_WIDTH

CIRCLE_TYPE = 1
RECT_TYPE = 2


class Renderer:

    space_bounds = []

    def __init__(self, parent):
        self.parent = parent
        self.joints_drawn = {}

    def init_physics(self):
        self.space = space = cymunk.Space()
        space.iterations = 30
        space.gravity = (0, -700)
        space.sleep_time_threshold = 0.5
        space.collision_slop = 0.5

        # create 4 segments that will act as a bounds
        for x in xrange(4):
            seg = cymunk.Segment(space.static_body,
                    cymunk.Vec2d(0, 0), cymunk.Vec2d(0, 0), 10.0)
            seg.elasticity = 0.6
            #seg.friction = 1.0
            self.space_bounds.append(seg)
            space.add(seg)

        # update bounds with good positions
        self.update_bounds()

    def update_bounds(self, *largs):
        assert(len(self.space_bounds) == 4)
        a, b, c, d = self.space_bounds
        x0, y0 = self.parent.pos
        x1 = self.parent.right
        y1 = self.parent.top
        space = self.space
        self.space.remove(a)
        self.space.remove(b)
        self.space.remove(c)
        self.space.remove(d)
        a = cymunk.Segment(space.static_body,
                    cymunk.Vec2d(x0, y0), cymunk.Vec2d(x1, y0), 10.0)
        b = cymunk.Segment(space.static_body,
                    cymunk.Vec2d(x1, y0), cymunk.Vec2d(x1, y1), 10.0)
        c = cymunk.Segment(space.static_body,
                    cymunk.Vec2d(x1, y1), cymunk.Vec2d(x0, y1), 10.0)
        d = cymunk.Segment(space.static_body,
                    cymunk.Vec2d(x0, y1), cymunk.Vec2d(x0, y0), 10.0)
        self.space.add(a)
        self.space.add(b)
        self.space.add(c)
        self.space.add(d)
        self.space_bounds = [a, b, c, d] 
        for x in self.space_bounds:
            x.friction = FRICTION

    def update_objects(self):
        for body in self.space.bodies:
            data = body.data
            p = body.position

            if data["type"]==CIRCLE_TYPE:
                rad = data["radius"]
                canvas_instruction = data["instruction"][0]

                canvas_instruction.pos = p.x-rad, p.y-rad
                canvas_instruction.size = rad*2, rad*2
            elif data["type"]==RECT_TYPE:
                rect, rotater, unrotater = data["instruction"]
                size = data["size"]

                rotater.angle = math.degrees(body.angle)
                rotater.origin = p.x, p.y
                rect.pos = p.x-(size[0]/2), p.y-(size[1]/2)
                rect.size = size
                unrotater.angle = -math.degrees(body.angle)
                unrotater.origin = p.x, p.y
            else: print body

        for joint in self.space.constraints:
            
            if isinstance(joint, cymunk.constraint.PivotJoint):
                pos = joint.anchor2["x"]-PIN_RADIUS,\
                      joint.anchor2["y"]-PIN_RADIUS
                if joint in self.joints_drawn:
                    pass
                else:
                    with self.parent.canvas:
                        Color(*get_rand_color(), mode="rgba")
                        self.joints_drawn[joint] = Ellipse(
                            pos=pos,
                            size=(2*PIN_RADIUS, 2*PIN_RADIUS))
            else:
                lpoints = [
                    joint.anchor1["x"], joint.anchor1["y"],
                    joint.anchor2["x"], joint.anchor2["y"]]
                if joint in self.joints_drawn:
                    self.joints_drawn[joint].points = lpoints
                else:
                    with self.parent.canvas:
                        Color(*get_rand_color(), mode="rgba")
                        self.joints_drawn[joint] = \
                            Line(points=lpoints,
                                 width=10)


    def add_circle(self, x, y, radius, random_color):
        body = cymunk.Body(100, 1e5)
        body.position = x, y
        circle = cymunk.Circle(body, radius)
        circle.elasticity = 0.6
        circle.friction = FRICTION/2
        self.space.add(body, circle)

        with self.parent.canvas.before:
            color = Color(*random_color, mode="rgba")
            rect = Ellipse(
                pos=(x-radius, y-radius),
                size=(radius*2, radius*2))
        body.data = {
            "radius": radius, 
            "color": color,
            "instruction": [rect],
            "type": CIRCLE_TYPE,
            "shapes": [circle]
        }

    def add_box(self, x, y, width, height, random_color):
        body = cymunk.Body(100., cymunk.moment_for_box(100., width, height))
        body.position = x, y

        rect_shape = cymunk.Poly.create_box(body, size=(width, height))
        rect_shape.elasticity = 0.6
        rect_shape.friction = FRICTION
        self.space.add(body, rect_shape)


        with self.parent.canvas.before:
            color = Color(*random_color, mode="rgba")
            rotater = Rotate(angle=0, axis=(0, 0, 1), origin=(x, y))
            rect = Rectangle(pos=(x-(width/2), y-(height/2)),
                             size=(width, height))
            unrotater = Rotate(0, (0, 0, 1), origin=(x, y))

        body.data = {
            "size": (width, height), 
            "color": color,
            "instruction": (rect, rotater, unrotater),
            "type": RECT_TYPE,
            "shapes": [rect_shape]
        }
