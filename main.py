from kivy.app import App
from kivy.uix.widget import Widget

from kivy.properties import ObjectProperty

from game import PhysicsGame
from tools import *


class PhysicsWidget(Widget):
    game = ObjectProperty(None)


class PhysicsApp(App):
    def build(self):
        return PhysicsWidget()


if __name__ == '__main__':
    PhysicsApp().run()
