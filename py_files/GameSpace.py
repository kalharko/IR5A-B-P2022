
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ListProperty, ReferenceListProperty, StringProperty,
    BooleanProperty
)
#import hell to be dealt with later
from py_files.TokenManager import *
from py_files.PingManager import *
from py_files.Map import *


class GameSpace(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)
    size = ListProperty([0,0])
    last_pos = ListProperty([0, 0])
    zoom = NumericProperty(1)
    touch_passed_on = BooleanProperty(False)

    def load_map(self, path) :
        self.map.load_texture(path)
        self.size = self.map.og_size

    def load_token(self, path):
        self.tokenManager.load_token(path, self.map.cell_size)

    # # Controls
    def on_touch_down(self, touch):
        # Tracks position of touch down
        self.last_pos = [touch.x, touch.y]

        # Tries to pass the touch to tokens
        if self.tokenManager.test_collision(touch.pos) != False :
            self.touch_passed_on = True

        # for token in self.tokens :
        #     if token.collide_point(*touch.pos):
        #         self.touch_passed_on = True

        if touch.is_double_tap :
            self.pingManager.on_touch_down(touch)

        # Zoom
        if touch.is_mouse_scrolling and self.map.texture != "":
            direction = 1 if touch.button == 'scrollup' else -1
            factor = 0.1;
            zoom = 1 * direction * factor;
            if self.zoom + zoom < 0.1 :
                return

            # compute the weights for x and y
            wx = (touch.x-self.x)/(self.map.og_size[0]*self.zoom);
            wy = (touch.y-self.y)/(self.map.og_size[1]*self.zoom);

            # apply the change in x,y and zoom.
            self.x -= wx*self.map.og_size[0]*zoom;
            self.y -= wy*self.map.og_size[1]*zoom;
            self.zoom += zoom;
            self.size[0] = int(self.map.og_size[0] * self.zoom)
            self.size[1] = int(self.map.og_size[1] * self.zoom)
            self.map.size = self.size
            self.map.cell_size = int(self.size[0] / self.map.grid_size[0])

            # moves and scale tokens
            self.tokenManager.move_scale(self.map.cell_size, self.pos)
            # for token in self.tokens :
            #     token.size[0] = self.map.cell_size
            #     token.size[1] = self.map.cell_size
            #     token.reposition(self.pos)


    def on_touch_move(self, touch):
        if self.touch_passed_on :
            self.tokenManager.touch_move_pass_on(touch)
            # for token in self.tokens :
            #     token.on_touch_move(touch)
        else :
            # Moves following mouse drag
            self.x += touch.x-self.last_pos[0]
            self.y += touch.y-self.last_pos[1]

            self.tokenManager.reposition_all(self.pos)
            # for token in self.tokens :
            #     token.reposition(self.pos)

            for ping in self.pingManager.children:
                ping.x += touch.x-self.last_pos[0]
                ping.y += touch.y-self.last_pos[1]

            self.last_pos = [touch.x, touch.y]

    def on_touch_up(self, touch):
        self.touch_passed_on = False
