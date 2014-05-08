from kivy.uix.widget import Widget
from random import random
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from renderer import Renderer
from tools import *

from kivy.lang import Builder
Builder.load_file('kv/game.kv')


PAUSED = 0
RUNNING = 1


class PhysicsGame(Widget):
    toolbox = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PhysicsGame, self).__init__(**kwargs)

        self.renderer = Renderer(self)
        self.game_state = RUNNING

        self.renderer.init_physics()
        self.bind(
            size=self.renderer.update_bounds,
            pos=self.renderer.update_bounds)

        self.tools = {}
        for t in all_tools:
            self.tools[t.name] = t(self)

        self.current_tool = self.tools["circle"]

        Clock.schedule_interval(self.step, 1 / 30.)

    def step(self, dt):
        if self.game_state==RUNNING:
            self.renderer.space.step(1 / 30.)
            self.renderer.update_objects()

    def on_touch_down(self, touch):
        self.current_tool.on_touch_down(touch)

    def on_touch_up(self, touch):
        self.current_tool.on_touch_up(touch)

    def on_touch_move(self, touch):
        self.current_tool.on_touch_move(touch)

    def set_tool(self, tool_name):
        self.current_tool = self.tools[tool_name]

    def toggle_game_state(self):
        self.game_state = RUNNING if self.game_state==PAUSED else PAUSED
