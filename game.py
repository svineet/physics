from kivy.uix.widget import Widget
from random import random
from kivy.clock import Clock

from renderer import Renderer
from tools import *

from kivy.lang import Builder
Builder.load_file('kv/game.kv')


class PhysicsGame(Widget):

    def __init__(self, **kwargs):
        super(PhysicsGame, self).__init__(**kwargs)

        self.renderer = Renderer(self)

        self.renderer.init_physics()
        self.bind(
            size=self.renderer.update_bounds,
            pos=self.renderer.update_bounds)
        Clock.schedule_interval(self.step, 1 / 30.)

        self.tools = {}
        for t in all_tools:
            self.tools[t.name] = t(self)

        self.current_tool = self.tools["rectangle"]

    def step(self, dt):
        self.renderer.space.step(1 / 30.)
        self.renderer.update_objects()

    def on_touch_down(self, touch):
        self.current_tool.on_touch_down(touch)

    def on_touch_up(self, touch):
        self.current_tool.on_touch_up(touch)

    def on_touch_move(self, touch):
        self.current_tool.on_touch_move(touch)

    def set_current_tool(tool_name):
        self.current_tool = self.tools[tool_name]
