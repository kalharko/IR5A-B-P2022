from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ColorProperty, ReferenceListProperty
)

from kivy.animation import Animation

class Ping(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)


class PingManager(Widget):
    bg_color = ColorProperty()
    sizeWanted = NumericProperty()


    def animation(self, widget, time, color):
        def destroy_widget(animate, widget):
            self.remove_widget(widget)

        animate = Animation(duration=0)
        for i in range (3):
            animate += Animation(
                bg_color = color,
                sizeWanted = 30,
                duration = time
            )
            animate += Animation(
                bg_color = (0, 0, 1, 1),
                sizeWanted = 15,
                duration = 1 - time
            )
        animate.repeat = False
        animate.start(widget)
        animate.bind(on_complete=destroy_widget)

    def on_touch_down(self, touch):
        # Ping instantiation
        # called when double-click on widget map
        ping = Ping()
        self.add_widget(ping)
        ping.pos = touch.pos
        self.animation(ping, 0.7, (1, 0, 0 ,1))
