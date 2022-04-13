# import hell to be delt with later
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy import require
from kivy.uix.image import Image

#from PIL import Image

require('2.1.0')


class Map(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)
    last_pos = ListProperty()

    texture = StringProperty("")
    size = ListProperty([0,0])

    def load_texture(self, path) :
        self.texture = path
        im = Image(source=path)
        self.size = im.texture_size
        #self.allow_stretch = False
        #self.keep_ratio = True


    # # Controls
    def on_touch_down(self, touch):
        # Tracks position of touch down
        self.last_pos = [touch.x, touch.y]

        # Zoom in on the map
        if touch.is_mouse_scrolling:
            # Transform touch.pos to parent's coordinates
            touch.push() # Did not understand the doc
            touch.apply_transform_2d(self.to_parent)
            if touch.button == 'scrolldown':
                self.x += (touch.x - self.x) * 0.1
                self.y += (touch.y - self.y) * 0.1
                self.size = (int(self.size[0]*0.9), int(self.size[1]*0.9))
            elif touch.button == 'scrollup':
                self.x -= (touch.x - self.x) * 0.1
                self.y -= (touch.y - self.y) * 0.1
                self.size = (int(self.size[0]*1.1), int(self.size[1]*1.1))
            touch.pop() # Did not understand the doc

    def on_touch_move(self, touch):
        # Moves canvas following mouse drag
        self.x += touch.x-self.last_pos[0]
        self.y += touch.y-self.last_pos[1]
        self.last_pos = touch.pos




class MainWidget(Widget):
    map = ObjectProperty(None)

    def update(self, dt): #dt as delta time ?
        pass





class VttApp(App):
    def build(self):
        mainWidget = MainWidget()

        # map initialization
        mainWidget.map.load_texture("Images/map_42x22.png")

        Clock.schedule_interval(mainWidget.update, 1.0 / 60.0)
        return mainWidget


if __name__ == '__main__':
    VttApp().run()



#  Image:
#         center:root.center
#         source: 'Images/map_42x22.png'
#         pos: self.pos
