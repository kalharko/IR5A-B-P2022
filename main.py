# import hell to be delt with later
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty, BooleanProperty
)
from kivy.graphics import Rectangle
from kivy.vector import Vector
from kivy.clock import Clock
from kivy import require
from kivy.uix.image import Image

#from PIL import Image

require('2.1.0')

class Token(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)
    grid_pos = ListProperty([0,0])
    texture = StringProperty("")
    size = ListProperty([0,0])

    def move(self, x, y=None):
        if y == None and type(x) in [type([]), type(())] :
            y = x[1]
            x = x[0]
        self.x += x
        self.y += y

    def set_grid_pos(self, parent_pos, cell_size=None, grid_pos=None):
        if grid_pos == None :
            grid_pos = self.grid_pos
        if cell_size == None :
            cell_size = self.size
        self.x = parent_pos[0] + cell_size[0] * grid_pos[0]
        self.x = parent_pos[1] + cell_size[1] * grid_pos[1]

    def on_touch_move(self, touch):
        self.x = touch.x - touch.x % self.size[0]
        self.y = touch.y - touch.y % self.size[1]
        self.grid_pos = [touch.x//self.size[0], touch.y//self.size[1]]


class Map(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)
    last_pos = ListProperty()
    zoom = NumericProperty(1)

    texture = StringProperty("")
    size = ListProperty([0,0])
    og_size = ListProperty([0,0])
    grid_size = ListProperty([42, 22])
    cell_size = ListProperty([0,0])

    tokens = ListProperty([])
    touch_passed_on = BooleanProperty(False)

    def load_texture(self, path, center=(0,0)):
        self.texture = path
        im = Image(source=path)
        self.og_size = im.texture_size
        self.size = im.texture_size
        self.cell_size = [self.size[0]//self.grid_size[0], self.size[1]//self.grid_size[1]]

    def load_token(self, path):
        self.tokens.append(Token(pos=self.pos, size=self.cell_size, texture=path))
        self.add_widget(self.tokens[-1])



    # # Controls
    def on_touch_down(self, touch):
        # Tries to pass the touch to childrens
        for token in self.tokens :
            if token.collide_point(*touch.pos):
                self.touch_passed_on = True

        # Tracks position of touch down
        self.last_pos = [touch.x, touch.y]

        # Zoom
        if touch.is_mouse_scrolling :
            if touch.button == 'scrolldown' :
                direction = -1
            else :
                direction = 1
            factor = 0.01;
            zoom = 1 * direction * factor;

            # compute the weights for x and y
            wx = (touch.x-self.x)/(self.og_size[0]*self.zoom);
            wy = (touch.y-self.y)/(self.og_size[1]*self.zoom);

            # apply the change in x,y and zoom.
            self.x -= wx*self.og_size[0]*zoom;
            self.y -= wy*self.og_size[1]*zoom;
            self.zoom += zoom;
            self.size[0] = int(self.og_size[0] * self.zoom)
            self.size[1] = int(self.og_size[1] * self.zoom)




    def on_touch_move(self, touch):
        if self.touch_passed_on :
            for token in self.tokens :
                token.on_touch_move(touch)
        else :
            # Moves canvas following mouse drag
            self.x += touch.x-self.last_pos[0]
            self.y += touch.y-self.last_pos[1]

            for token in self.tokens :
                token.x += touch.x-self.last_pos[0]
                token.y += touch.y-self.last_pos[1]

            self.last_pos = touch.pos

    def on_touch_up(self, touch):
        self.touch_passed_on = False








class MainWidget(Widget):
    map = ObjectProperty(None)

    def update(self, dt): #dt as delta time ?
        pass





class VttApp(App):
    def build(self):
        mainWidget = MainWidget()

        # map initialization
        mainWidget.map.load_texture("Images/map_42x22.png")
        mainWidget.map.load_token("Images/Token_Red_1.png")

        Clock.schedule_interval(mainWidget.update, 1.0 / 60.0)
        return mainWidget


if __name__ == '__main__':
    VttApp().run()



#  Image:
#         center:root.center
#         source: 'Images/map_42x22.png'
#         pos: self.pos
