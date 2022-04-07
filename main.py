from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy import require

require('2.1.0')


class Map(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)



class MainWidget(Widget):
    map = ObjectProperty(None)

    def update(self, dt): #dt as delta time ?
        pass

    def on_touch_down(self, touch):
        self.map.center = (0,0)
        pass


class VttApp(App):
    def build(self):
        mainWidget = MainWidget()
        Clock.schedule_interval(mainWidget.update, 1.0 / 60.0)
        return mainWidget


if __name__ == '__main__':
    VttApp().run()



