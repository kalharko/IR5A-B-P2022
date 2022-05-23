# import hell to be delt with later
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty, BooleanProperty
)
from kivy.graphics import Rectangle
from kivy.vector import Vector
from kivy.animation import Animation
from kivy.clock import Clock
from kivy import require
from kivy.uix.image import Image

#Connectivity imports
#from server import VttServer
from threading import Thread, Lock
#import client

from os import path



require('2.1.0')

## Include our own classes :
import sys
#sys.path.append('./py_files')
#from FileChooserPopup import FileChooserPopup

## Include all our classes :
import os
for entry in os.scandir('py_files'):
    if entry.is_file():
        string = f'from py_files.{entry.name[:-3]} import *'
        exec (string)


## Include all the kv files
from kivy.lang import Builder
from os import listdir
kv_path = "./kv_files/"
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)




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








class GameSpace(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)
    size = ListProperty([0,0])
    last_pos = ListProperty([0, 0])
    zoom = NumericProperty(1)

    tokens = ListProperty([])
    touch_passed_on = BooleanProperty(False)

    def load_map(self, path) :
        self.map.load_texture(path)
        self.size = self.map.og_size

    def load_token(self, path):
        self.tokens.append(Token(grid_pos=[0,0], size=[self.map.cell_size,self.map.cell_size], texture=path))
        self.add_widget(self.tokens[-1])
        self.tokens[-1].reposition(self.pos)

    # # Controls
    def on_touch_down(self, touch):
        # Tracks position of touch down
        self.last_pos = [touch.x, touch.y]

        # Tries to pass the touch to childrens
        for token in self.tokens :
            if token.collide_point(*touch.pos):
                self.touch_passed_on = True

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
            for token in self.tokens :
                token.size[0] = self.map.cell_size
                token.size[1] = self.map.cell_size
                token.reposition(self.pos)


    def on_touch_move(self, touch):
        if self.touch_passed_on :
            for token in self.tokens :
                token.on_touch_move(touch)
        else :
            # Moves following mouse drag
            self.x += touch.x-self.last_pos[0]
            self.y += touch.y-self.last_pos[1]

            for token in self.tokens :
                token.reposition(self.pos)

            for ping in self.pingManager.children:
                ping.x += touch.x-self.last_pos[0]
                ping.y += touch.y-self.last_pos[1]

            self.last_pos = [touch.x, touch.y]

    def on_touch_up(self, touch):
        self.touch_passed_on = False







class MainWidget(Widget):
    role = StringProperty(0)
    map = ObjectProperty(None)

    def server_setup(self):
        # server
        server_lock = Lock()
        server = VttServer('Data/game', server_lock)
        #mainWidget.server_lock = server_lock
        t = Thread(target=server.run)
        t.start()

    def load_game(self, name):
        # map initialization
        self.gameSpace.load_map("Images/map_42x22.png")
        self.gameSpace.load_token("Images/Token_Red_1.png")
        #self.add_widget(self.gameSpace) #necessary ?
        print("game loaded")

    def update(self, dt): #dt as delta time ?
        pass



class FirstMenuPopup(Popup):
    path = StringProperty(path.abspath('.'))
    def launch_as_Player(self):
        self.dismiss()

    def launch_as_GM(self):
        self.dismiss()

    def open_file_chooser(self):
        file_chooser = FileChooserPopup()
        file_chooser.open()
        file_chooser.bind(on_dismiss=self.popup_set_path)

        file_chooser.file_chooser.path = path.abspath('.')

    def popup_set_path(self, popup):
        self.path = popup.file_chooser.path




class VttApp(App):
    def build(self):
        self.mainWidget = MainWidget()
        self.mainWidget.map = Map()
        popup = FirstMenuPopup()
        popup.open()
        popup.bind(on_dismiss=self.mainWidget.load_game)

        Clock.schedule_interval(self.mainWidget.update, 1.0 / 60.0)
        return self.mainWidget


if __name__ == '__main__':
    VttApp().run()


