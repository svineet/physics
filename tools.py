import pymunk as cymunk
from pymunk import Vec2d

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView

from kivy.graphics import Ellipse, Color, Line, Rectangle, Triangle
from kivy.utils import get_color_from_hex

from kivy.lang import Builder
Builder.load_file('kv/tools.kv')

import utils

LINE_WIDTH = 1.1
MOTOR_VELOCITY = -50


class Tool:
    name = "default"
    icon = "resources/wrench.png"

    def __init__(self, game):
        self.game = game

    def draw(self,x, y):
        pass

    def on_touch_down(self, touch):
        pass

    def on_touch_up(self, touch):
        pass

    def on_touch_move(self, touch):
        self.draw(touch.x, touch.y)


class CircleTool(Tool):
    name = "Circle"
    icon = "resources/circle.svg"
    help_text = "Drag and draw!"

    def __init__(self, game):
        self.game = game

        self.draw_circle = None
        self.draw_line = None

        self.init_pos = None
        self.final_pos = None
        self.saved = None

    def draw(self, x, y):
        d = int(utils.distance((x, y), self.init_pos))
        x1, y1 = self.init_pos

        if self.draw_circle is not None:

            self.draw_circle.pos = (x1-d, y1-d)
            self.draw_circle.size = (2*d, 2*d)

            self.draw_line.points = [x1, y1, x, y]
        else:
            with self.game.canvas:
                self.color = utils.random_color()
                Color(*self.color, mode="rgba")
                self.draw_circle = \
                    Ellipse(pos=(x+d, y+d),
                            size=(d/2, d/2))
                
                Color(*get_color_from_hex("#33B5E5"))
                self.draw_line = \
                    Line(points=[x1, y1, x, y],
                         width=LINE_WIDTH, cap="round")



    def on_touch_down(self, touch):
        self.init_pos = touch.x, touch.y

    def on_touch_up(self, touch):
        if self.init_pos is None:
            return

        self.final_pos = touch.x, touch.y
        x1, y1 = self.init_pos
        d = int(utils.distance(self.final_pos, self.init_pos))
        
        if not (d<10):
            self.game.renderer.add_circle(x1, y1, d, self.color)
            self.saved = d
        elif self.saved is not None:
            # Add saved one
            d = self.saved
            x1, y1 = touch.x, touch.y

            self.game.renderer.add_circle(x1, y1, d, self.color)

        if self.draw_circle is not None and self.draw_line is not None:
            self.game.canvas.remove(self.draw_circle)
            self.game.canvas.remove(self.draw_line)

        self.draw_circle = None
        self.draw_line = None
        self.init_pos = None
        self.final_pos = None


class RectangleTool(Tool):
    name = "Rectangle"
    icon = "resources/circle.svg"
    help_text = "Drag and draw!"

    def __init__(self, game):
        self.game = game

        self.draw_rectangle = None
        self.draw_line = None

        self.init_pos = None
        self.saved = None

    def draw(self, x, y):
        d = int(utils.distance((x, y), self.init_pos))
        x1, y1 = self.init_pos

        if self.draw_rectangle is not None:
            hw = abs(x1-x)
            hh = abs(y1-y)
            self.draw_rectangle.pos = (x1-hw, y1-hh)
            self.draw_rectangle.size = (2*hw, 2*hh)

            self.draw_line.points = [x1, y1, x, y]
        else:
            with self.game.canvas:
                self.color = utils.random_color()
                Color(*self.color, mode="rgba")

                self.draw_rectangle = \
                    Rectangle(pos=(x-d, y-d),
                              size=(d/2, d/2))
                
                Color(*get_color_from_hex("#33B5E5"), mode="rgba")
                self.draw_line = \
                    Line(points=[x1, y1, x, y],
                         width=LINE_WIDTH, cap="round")

    def on_touch_down(self, touch):
        self.init_pos = touch.x, touch.y

    def on_touch_up(self, touch):
        if self.init_pos is None:
            return

        x, y = touch.x, touch.y
        x1, y1 = self.init_pos
        hw = abs(x1-x)
        hh = abs(y1-y)

        if not (hw<5 or hh<5):  
            self.game.renderer.add_box(x1, y1, 2*hw, 2*hh, self.color)
            self.saved = (hw, hh)
        elif self.saved is not None:
            # Add saved one
            hw, hh = self.saved
            x1, y1 = touch.x, touch.y

            self.game.renderer.add_box(x1, y1, 2*hw, 2*hh, self.color)

        if self.draw_rectangle is not None and self.draw_line is not None:
            self.game.canvas.remove(self.draw_rectangle)
            self.game.canvas.remove(self.draw_line)

        self.draw_rectangle = None
        self.draw_line = None
        self.init_pos = None
        self.final_pos = None


class TriangleTool(Tool):
    name = """Triangle
[color=ff0000]Experimental[/color]"""
    icon = "resources/circle.svg"
    help_text = "Drag and draw!"

    def __init__(self, game):
        self.game = game

        self.draw_altitude = None
        self.draw_triangle = None

        self.init_pos = None
        self.final_pos = None
        self.saved = None

    def draw(self, x, y):
        x1, y1 = self.init_pos

        if self.draw_triangle is not None:
            mouse_x_y = x, y

            vertices = utils.constructTriangleFromLine(self.init_pos, mouse_x_y)
            self.draw_triangle.points = vertices
            self.draw_altitude.points = [x, y, x1, y1]
        else:
            with self.game.canvas:
                self.color = utils.random_color()
                Color(*self.color, mode="rgba")
                self.draw_triangle = Triangle(
                    points=utils.get_triangle_points(x1, y1, x, y))
                Color(*utils.random_color(), mode="rgba")
                self.draw_altitude = \
                    Line(points=[x1, y1, x, y],
                         width=LINE_WIDTH, cap="square")



    def on_touch_down(self, touch):
        self.init_pos = touch.x, touch.y

    def on_touch_up(self, touch):
        if self.init_pos is None:
            return

        self.final_pos = touch.x, touch.y
        x1, y1 = self.init_pos
        d = int(utils.distance(self.final_pos, self.init_pos))
        
        mouse_x_y = touch.x, touch.y
        if d>20:
            vertices = utils.constructTriangleFromLine(self.init_pos,
                                                   mouse_x_y)
            self.game.renderer.add_triangle(vertices, self.color)
            self.saved = d
        elif self.saved is not None:
            vertices = utils.constructTriangleFromLine(
                self.init_pos,
                (self.init_pos[0], self.init_pos[1]-self.saved))
            self.game.renderer.add_triangle(vertices, self.color)

        if self.draw_altitude is not None and self.draw_triangle is not None:
            self.game.canvas.remove(self.draw_altitude)
            self.game.canvas.remove(self.draw_triangle)

        self.draw_altitude = None
        self.draw_triangle = None
        self.init_pos = None
        self.final_pos = None


class PinTool(Tool):
    name = "Pin"
    icon = "resources/pin.png"
    help_text = "Click and pin the object to the place!"

    def __init__(self, game):
        self.game = game

    def draw(self, x, y):
        pass

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        space = self.game.get_space()
        shape = space.point_query_first(Vec2d(x, y))
        if shape is None:
            print "lel u iz mudi egent or wat? i wll roit ur houze fr da lulz."+\
                  " heuhuehhue"
        else:
            body = shape.body
            joint = cymunk.constraint.PivotJoint(body,
                                             space.static_body,
                                             Vec2d(x, y))

            space.add(joint)


class MotorTool(Tool):
    name = "Motor"
    icon = "resources/pin.png"
    help_text = "Click and see it spin!"

    def __init__(self, game):
        self.game = game

    def draw(self, x, y):
        pass

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        space = self.game.get_space()
        shape = space.point_query_first(Vec2d(x, y))
        if shape is None:
            print "lel u iz mudi egent or wat? i wll roit ur houze fr da lulz."+\
                  " heuhuehhue"
        else:
            body = shape.body
            joint = cymunk.constraint.SimpleMotor(body,
                                             space.static_body,
                                             MOTOR_VELOCITY)
            joint2 = cymunk.constraint.PivotJoint(body,
                                             space.static_body,
                                             Vec2d(x, y))

            space.add([joint, joint2])



class JointTool(Tool):
    name = "Joint"
    icon = "resources/joint.png"
    help_text = "Attach two things together!"

    def __init__(self, game):
        self.game = game
        self.space = self.game.get_space()
        self.draw_line = None

        self.clean_up()

    def draw(self, x, y):
        if self.draw_line is not None:
            self.draw_line.points = [self.init_pos[0], self.init_pos[1], x, y]
        elif self.init_pos:
            with self.game.canvas.after:
                Color(*utils.random_color(), mode="rgba")
                self.draw_line = \
                    Line(points=[self.init_pos[0], self.init_pos[1], x, y],
                         width=LINE_WIDTH)

    def on_touch_down(self, touch):
        shape = self.space.point_query_first(Vec2d(touch.x, touch.y))
        if shape is None:
            print "lel u iz mudi egent or wat? i wll roit ur houze fr da lulz."+\
                  " heuhuehhue"
            self.clean_up()
        else:
            self.init_pos = (touch.x, touch.y)
            self.body1 = shape.body

    def on_touch_up(self, touch):
        shape = self.space.point_query_first(Vec2d(touch.x, touch.y))
        if shape is None:
            print "lel u iz mudi egent or wat? i wll roit ur houze fr da lulz."+\
                  " heuhuehhue"
        else:
            self.final_pos = (touch.x, touch.y)
            self.body2 = shape.body

            ix, iy = self.init_pos
            fx, fy = self.final_pos
            x1, y1 = self.body1.position.x, self.body1.position.y
            x2, y2 = self.body2.position.x, self.body2.position.y
            anchr1 = (ix-x1, iy-y1)
            anchr2 = (fx-x2, fy-y2)


            joint = cymunk.PinJoint(
                self.body1, self.body2,
                anchr1, anchr2
                )

            self.space.add(joint)
        self.clean_up()

    def clean_up(self):
        self.init_pos = None
        self.body1 = None
        self.final_pos = None
        self.body2 = None

        if self.draw_line is not None:
            self.game.canvas.after.remove(self.draw_line)
            # print "Removed that shitty line"

        self.draw_line = None


class GrabTool(Tool):
    name = "Grab"
    icon = "resources/grab.png"
    help_text = "Drag things around (Only works in Paused mode)"

    def __init__(self, game):
        self.game = game
        self.space = self.game.get_space()
        self.draw_line = None

        self.clean_up()

    def draw(self, x, y):
        pass

    def on_touch_down(self, touch):
        pass

    def on_touch_up(self, touch):
        
        self.clean_up()

    def on_touch_move(self, touch):
        if not self.delta: return

    def clean_up(self):
        self.init_pos = None
        self.body1 = None
        self.final_pos = None
        self.body2 = None

        if self.draw_line is not None:
            self.game.canvas.after.remove(self.draw_line)
            # print "Removed that shitty line"

        self.draw_line = None


class AntiGravityTool(Tool):
    name = "Anti Gravity"
    icon = "resources/gravity.png"
    help_text = "import antigravity"

    def __init__(self, game):
        self.game = game

    def click_button_cb(self):
        gnow = self.game.get_space().gravity[1]
        self.game.get_space().gravity = (0, -gnow)
        # print gnow
        for b in self.game.get_space().bodies:
            b.activate()


class EraserTool(Tool):
    name = "Eraser"
    icon = "resources/pin.png"
    help_text = "Drag and destroy everything in your path!"

    def __init__(self, game):
        self.game = game
        self.draw_vertices = []
        self.draw_line = None

    def draw(self):
        if self.draw_line is None:
            with self.game.canvas:
                Color(*utils.random_color(), mode="rgba")
                self.draw_line = Line(points=self.draw_vertices,
                                      width=3)
        else:
            self.draw_line.points = self.draw_vertices

    def on_touch_up(self, touch):
        self.draw_vertices = []
        if self.draw_line: self.game.canvas.remove(self.draw_line)
        self.draw_line = None

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        space = self.game.get_space()
        shape = space.point_query_first(Vec2d(x, y))
        if shape is None:
            pass
        else:
            body = shape.body
            

            if not hasattr(body, 'data'):
                return

            data = body.data
            check_joints = False
            j = None
            for c in space.constraints[::-1]:
                if c.a is body or c.b is body:
                    check_joints = True
                    j = c
                    if not isinstance(j, cymunk.constraint.SimpleMotor):
                        self.game.canvas.remove(
                            self.game.renderer.joints_drawn[j])
                        del self.game.renderer.joints_drawn[j]
                    break

            if check_joints:
                space.remove(j)
            else:
                # print "Nope"
                for s in data["shapes"]:
                    space.remove(s)

                for ins in data["instruction"]:
                    self.game.canvas.before.remove(ins)
                space.remove(body)

    def on_touch_move(self, touch):
        if len(self.draw_vertices)>18:
            self.draw_vertices.pop(0)
            self.draw_vertices.pop(0)
        self.draw_vertices.extend([touch.x, touch.y])
        if len(self.draw_vertices)>2:
            self.draw()

        self.on_touch_down(touch)


class EraseAllTool(Tool):
    name = "Erase All"
    icon = "resources/gravity.png"
    help_text = "Destroyed them all!"

    def __init__(self, game):
        self.game = game

    def click_button_cb(self):
        space = self.game.get_space()

        for b in space.bodies:
            # print b
            ins = b.data["instruction"]
            for i in ins:
                self.game.canvas.before.remove(i)
            space.remove(b)

        for c in space.constraints:
            if c in self.game.renderer.joints_drawn:
                self.game.canvas.remove(self.game.renderer.joints_drawn[c])
                del self.game.renderer.joints_drawn[c]
            space.remove(c)

        for s in space.shapes:
            space.remove(s)

        self.game.renderer.update_bounds(new=True)


all_tools = [
    CircleTool,
    RectangleTool,
    TriangleTool,
    PinTool,
    MotorTool,
    JointTool,
    AntiGravityTool,
    EraserTool,
    EraseAllTool
]


from kivy.properties import ObjectProperty
class SublimeButton(Button):
    on_press1 = ObjectProperty(lambda *a: a)
    def_color = [1, 0.7, 0, 0]

    def __init__(self, **kw):
        super(SublimeButton, self).__init__(**kw)

    def activated(self):
        self.background_color = \
            [0.2, 0.7098039215686275, 0.8980392156862745, 0.7]

    def deactivated(self):
        self.on_press1()
        self.background_color = self.def_color


from functools import partial
class ToolBox(BoxLayout):

    def __init__(self, **kw):
        super(ToolBox, self).__init__(**kw)

        revealer = SublimeButton(
            text="Tools",
            size_hint=(0.8 ,1),
            on_press1=self.toggle_tool_visible)

        self.add_widget(revealer)
        
        self.tools_visible = False

        self.scroller = ScrollView(size_hint=(1, 1))

        self.scroll_box = GridLayout(rows=1, size_hint=(None, 1))
        self.scroll_box.bind(
            minimum_width=self.scroll_box.setter('width'))

        pause_res = SublimeButton(text="Pause")
        pause_res.on_press1 = self.toogle_game_play_pause
        self.pause_res = pause_res
        self.scroll_box.add_widget(pause_res)

        for tool in all_tools:
            b = SublimeButton()
            b.text = tool.name
            b.on_press1=partial(self.button_cb, tool.name)

            self.scroll_box.add_widget(b)
        self.scroller.add_widget(self.scroll_box)

    def button_cb(self, tool_name, *args):
        game = self.parent.parent.ids.game
        if hasattr(game.tools[tool_name], 'click_button_cb'):
            game.tools[tool_name].click_button_cb()
        else:
            game.set_tool(tool_name)
        game.show_help_text(game.tools[tool_name].help_text)

    def toggle_tool_visible(self, *args):
        if self.tools_visible:
            self.remove_widget(self.scroller)
            self.tools_visible = False
        elif not self.tools_visible:
            self.add_widget(self.scroller)
            self.tools_visible = True

    def toogle_game_play_pause(self, *args):
        game = self.parent.parent.ids.game
        game.toggle_game_state()
        if game.game_paused()==1:
            self.pause_res.text = "Pause"
        else:
            self.pause_res.text = "Resume"
