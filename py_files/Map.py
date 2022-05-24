from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ListProperty, StringProperty
)

from kivy.uix.image import Image

class Map(Widget):
    texture = StringProperty("")
    og_size = ListProperty([0,0])
    grid_size = ListProperty([42, 22])
    cell_size = NumericProperty()
    size = ListProperty([0,0])


    def load_texture(self, path):
        self.texture = path
        im = Image(source=path)
        self.og_size = im.texture_size
        self.size = self.og_size
        self.cell_size = im.texture_size[0]//self.grid_size[0]
