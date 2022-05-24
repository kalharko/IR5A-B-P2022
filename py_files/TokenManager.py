from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ListProperty, ReferenceListProperty, StringProperty
)

from kivy.animation import Animation
from kivy.uix.image import Image

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
    tokens = ListProperty([])

    def load_token(self, path, cell_size):
        self.tokens.append(Token(grid_pos=[0,0], size=[cell_size,cell_size], texture=path))
        self.add_widget(self.tokens[-1])
        self.tokens[-1].reposition(self.pos)

    def move_scale(self, cell_size, position) :
        for token in self.tokens :
            token.size[0] = cell_size[0]
            token.size[1] = cell_size[1]
            token.reposition(position)

    def test_collision(self, position) :
        for token in self.tokens :
            if token.collide_point(*position):
                return token
        return False

    def touch_move_pass_on(self, touch) :
        for token in self.tokens :
            token.on_touch_move(touch)

    def reposition_all(self, position) :
        for token in self.tokens :
            token.reposition(position)

