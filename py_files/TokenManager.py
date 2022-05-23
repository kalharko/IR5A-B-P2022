from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ListProperty, ReferenceListProperty, StringProperty
)

from kivy.animation import Animation

class Token(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)
    grid_pos = ListProperty([0,0])
    grid_origin = ListProperty([0,0])
    texture = StringProperty("")
    size = ListProperty([0,0])


    def reposition(self, grid_origin=None):
        if grid_origin != None :
            self.grid_origin = grid_origin

        self.x = self.grid_origin[0] + self.size[0] * self.grid_pos[0]
        self.y = self.grid_origin[1] + self.size[1] * self.grid_pos[1]

    def on_touch_move(self, touch):
        # self.pos = touch.pos
        # self.x = touch.x - self.size[0] // 2
        # self.y = touch.y - self.size[1] // 2

        self.grid_pos[0] = (touch.x - self.grid_origin[0]) // self.size[0]
        self.grid_pos[1] = (touch.y - self.grid_origin[1]) // self.size[1]
        self.reposition()



class TokenManager(Widget):
    pass #TO DO
