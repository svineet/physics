import math
import pymunk as cymunk
from pymunk import Vec2d

from kivy.graphics import Color, Ellipse, Rectangle, Rotate, Line, Triangle
from kivy.properties import DictProperty, ListProperty

from utils import random_color as get_rand_color
from utils import distance, calc_center

FRICTION = 0.5
PIN_RADIUS = 4
from tools import LINE_WIDTH

CIRCLE_TYPE = 1
RECT_TYPE = 2
TRIANGLE_TYPE = 3


class Renderer:

    space_bounds = []
    bound_rects = []

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
        for x in xrange(2):
            seg = cymunk.Segment(space.static_body,
                    Vec2d(0, 0), Vec2d(0, 0), 10.0)
            seg.elasticity = 0.6
            #seg.friction = 1.0
            self.space_bounds.append(seg)
            space.add(seg)

        # update bounds with good positions
        self.update_bounds()

    def update_bounds(self, new=False, *largs):
        assert(len(self.space_bounds) == 2)
        a, b = self.space_bounds
        x0, y0 = self.parent.pos
        x1 = self.parent.right
        y1 = self.parent.top
        space = self.space
        if not new:
            self.space.remove(a)
            self.space.remove(b)
        a = cymunk.Segment(space.static_body,
                    Vec2d(x0, y0), Vec2d(x1, y0), 10.0)
        b = cymunk.Segment(space.static_body,
                    Vec2d(x1, y1), Vec2d(x0, y1), 10.0)
        self.space.add(a)
        self.space.add(b)
        self.space_bounds = [a, b] 
        for x in self.space_bounds:
            x.friction = FRICTION

    def update_objects(self):
        for body in self.space.bodies:
            data = body.data
            # print body
            p = body.position

            if data["type"]==CIRCLE_TYPE:
                rad = data["radius"]
                canvas_instruction, rot, unrot = data["instruction"]

                rot.angle = math.degrees(body.angle)
                rot.origin = p.x, p.y

                canvas_instruction.pos = p.x-rad, p.y-rad
                canvas_instruction.size = rad*2, rad*2

                unrot.angle = -math.degrees(body.angle)
                unrot.origin = p.x, p.y
            elif data["type"]==RECT_TYPE:
                rect, rotater, unrotater = data["instruction"]
                size = data["size"]

                rotater.angle = math.degrees(body.angle)
                rotater.origin = p.x, p.y
                rect.pos = p.x-(size[0]/2), p.y-(size[1]/2)
                rect.size = size
                unrotater.angle = -math.degrees(body.angle)
                unrotater.origin = p.x, p.y
            elif data["type"]==TRIANGLE_TYPE:
                rect, rotater, unrotater = data["instruction"]
                vertices = data["shapes"][0].get_vertices()
                center = cymunk.util.calc_center(vertices)
                # print 
                # print center
                # print (p.x, p.y)

                rotater.angle = math.degrees(body.angle)
                rotater.origin = center

                points2 = []
                for t in vertices:
                    points2.extend([t.x, t.y])

                rect.points = points2
                unrotater.angle = -math.degrees(body.angle)
                unrotater.origin = center
            else: print body

        for joint in self.space.constraints:
            # print joint.anchr1, joint.anchr2
            if isinstance(joint, cymunk.constraint.PivotJoint):
                pos = joint.anchr2.x-PIN_RADIUS,\
                      joint.anchr2.y-PIN_RADIUS
                if joint in self.joints_drawn:
                    self.joints_drawn[joint].pos = pos
                else:
                    with self.parent.canvas:
                        Color(*get_rand_color(), mode="rgba")
                        self.joints_drawn[joint] = Ellipse(
                            pos=pos,
                            size=(2*PIN_RADIUS, 2*PIN_RADIUS))
            elif isinstance(joint, cymunk.constraint.SimpleMotor):
                pass
            else:
                lpoints = [
                    joint.a.position.x+joint.anchr1.x, 
                        joint.a.position.y+joint.anchr1.y,
                    joint.b.position.x+joint.anchr2.x, 
                        joint.b.position.y+joint.anchr2.y]
                # print lpoints
                if joint in self.joints_drawn:
                    self.joints_drawn[joint].points = lpoints
                else:
                    with self.parent.canvas:
                        Color(*get_rand_color(), mode="rgba")
                        self.joints_drawn[joint] = \
                            Line(points=lpoints,
                                 width=LINE_WIDTH)
                        # print "added a line"


    def add_circle(self, x, y, radius, random_color):
        body = cymunk.Body(100, 1e5)
        body.position = x, y
        circle = cymunk.Circle(body, radius)
        circle.elasticity = 0.6
        circle.friction = FRICTION/2
        self.space.add(body, circle)

        with self.parent.canvas.before:
            color = Color(*random_color, mode="rgba")
            rot = Rotate(angle=0, axis=(0, 0, 1), origin=(x, y))
            rect = Ellipse(
                pos=(x-radius, y-radius),
                size=(radius*2, radius*2))
            unrot = Rotate(0, (0, 0, 1), origin=(x, y))
        body.data = {
            "radius": radius, 
            "color": color,
            "instruction": [rect, rot, unrot],
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

    def add_triangle(self, vertices, random_color):
        vbackup = vertices
        vertices  = zip(vertices[::2], vertices[1::2])
        center = cymunk.util.calc_center(vertices)
        body = cymunk.Body(100,
            cymunk.moment_for_poly(100, vertices))
        triangle = cymunk.Poly(body, vertices)
        triangle.elasticity = 0.6
        triangle.friction = FRICTION
        self.space.add(body, triangle)

        with self.parent.canvas.before:
            color = Color(*random_color, mode="rgba")
            rot = Rotate(angle=0, axis=(0, 0, 1), origin=center)
            triangle_shape = Triangle(points=vbackup)
            unrot = Rotate(0, (0, 0, 1), origin=center)
        body.data = {
            "color": color,
            "instruction": [triangle_shape, rot, unrot],
            "type": TRIANGLE_TYPE,
            "shapes": [triangle],
        }    
