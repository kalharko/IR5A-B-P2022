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


