import pymunk as cymunk
from pymunk import Vec2d

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior

from kivy.graphics import Ellipse, Color, Line, Rectangle
from kivy.utils import get_color_from_hex

from kivy.lang import Builder
Builder.load_file('kv/tools.kv')

import utils

LINE_WIDTH = 1.1


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
    name = "circle"
    icon = "resources/circle.svg"

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
    name = "rectangle"
    icon = "resources/circle.svg"

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


class PinTool(Tool):
    name = "pin"
    icon = "resources/pin.png"

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



class JointTool(Tool):
    name = "joint_tool"
    icon = "resources/joint.png"

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




class EraserTool(Tool):
    name = "eraser"
    icon = "resources/pin.png"

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
            for c in space.constraints:
                if c.a is body or c.b is body:
                    check_joints = True
                    j = c
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


all_tools = [
    CircleTool,
    RectangleTool,
    PinTool,
    JointTool,
    EraserTool
]
total_btns = len(all_tools)+1


class SublimeButton(Button):
    def __init__(self, **kw):
        super(SublimeButton, self).__init__(**kw)

        self.background_color = [0, 0, 0, 0]

    def activated(self):
        # self.background_color = 
        pass


from functools import partial
class ToolBox(BoxLayout):

    def __init__(self, **kw):
        super(ToolBox, self).__init__(**kw)

        self.tools_visible = False
        pause_res = SublimeButton(
            text="Pause/Resume",
            on_press=self.toogle_game_play_pause)
        self.tool_btns = [pause_res]
        for tool in all_tools:
            b = SublimeButton()
            b.text = tool.name
            b.bind(on_press=partial(self.button_cb, tool.name))
            self.tool_btns.append(b)

    def button_cb(self, tool_name, *args):
        self.parent.parent.ids.game.set_tool(tool_name)

    def toggle_tool_visible(self):
        if self.tools_visible:
            for btn in self.tool_btns:
                self.remove_widget(btn)
            self.width = self.ids.revealer.width+2
            self.tools_visible = False
        elif not self.tools_visible:
            for btn in self.tool_btns:
                self.add_widget(btn)
            self.tools_visible = True

    def toogle_game_play_pause(self, *args):
        self.parent.parent.ids.game.toggle_game_state()

