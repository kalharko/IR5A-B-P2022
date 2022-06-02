from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ListProperty, ReferenceListProperty, StringProperty
)

from kivy.animation import Animation
from kivy.uix.image import Image

class Bubble(Widget):
    texture = StringProperty("")
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)
    size = ListProperty([0,0])

class BubbleManager(Widget):
    bubbles = ListProperty([])

    def load_bubble(self, path, cell_size):
        self.bubbles.append(Bubble(texture= path, size= [cell_size, cell_size], pos= [cell_size*len(self.bubbles), 0]))
        self.add_widget(self.bubbles[len(self.bubbles) - 1])