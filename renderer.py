import cymunk as cy
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import DictProperty, ListProperty

CIRCLE_TYPE = 1
RECT_TYPE = 2


class Renderer:

    space_bounds = []

    def __init__(self, parent):
        self.parent = parent

    def init_physics(self):
        self.space = space = cy.Space()
        space.iterations = 30
        space.gravity = (0, -700)
        space.sleep_time_threshold = 0.5
        space.collision_slop = 0.5

        # create 4 segments that will act as a bounds
        for x in xrange(4):
            seg = cy.Segment(space.static_body,
                    cy.Vec2d(0, 0), cy.Vec2d(0, 0), 10.0)
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
        a = cy.Segment(space.static_body,
                    cy.Vec2d(x0, y0), cy.Vec2d(x1, y0), 10.0)
        b = cy.Segment(space.static_body,
                    cy.Vec2d(x1, y0), cy.Vec2d(x1, y1), 10.0)
        c = cy.Segment(space.static_body,
                    cy.Vec2d(x1, y1), cy.Vec2d(x0, y1), 10.0)
        d = cy.Segment(space.static_body,
                    cy.Vec2d(x0, y1), cy.Vec2d(x0, y0), 10.0)
        self.space.add(a)
        self.space.add(b)
        self.space.add(c)
        self.space.add(d)
        self.space_bounds = [a, b, c, d] 

    def update_objects(self):
        for body in self.space.bodies:
            data = body.data
            p = body.position

            if data["type"]==CIRCLE_TYPE:
                rad = data["radius"]
                canvas_instruction = data["instruction"]

                canvas_instruction.pos = p.x-rad, p.y-rad
                canvas_instruction.size = rad*2, rad*2
            elif data["type"]==RECT_TYPE:
                canvas_instruction = data["instruction"]
                size = data["size"]

                canvas_instruction.pos = p.x-(size[0]/2), p.y-(size[1]/2)
                canvas_instruction.size = size

    def add_circle(self, x, y, radius, random_color):
        body = cy.Body(100, 1e9)
        body.position = x, y
        circle = cy.Circle(body, radius)
        circle.elasticity = 0.6
        self.space.add(body, circle)

        with self.parent.canvas.before:
            color = Color(*random_color, mode="rgba")
            rect = Ellipse(
                pos=(x-radius, y-radius),
                size=(radius*2, radius*2))
        body.data = {
            "radius": radius, 
            "color": color,
            "instruction": rect,
            "type": CIRCLE_TYPE
        }

    def add_box(self, x, y, width, height, random_color):
        body = cy.Body(100., cy.moment_for_box(100., width, height))
        body.position = x, y

        rect_shape = cy.Poly.create_box(body, size=(width, height))
        rect_shape.elasticity = 0.6
        self.space.add(body, rect_shape)


        with self.parent.canvas.before:
            color = Color(*random_color, mode="rgba")
            rect = Rectangle(pos=(x, y),
                             size=(width, height))

        body.data = {
            "size": (width, height), 
            "color": color,
            "instruction": rect,
            "type": RECT_TYPE
        }
