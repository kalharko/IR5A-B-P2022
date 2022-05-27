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

import queue

from py_files.ClientConnection import ClientConnection


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
    game_path = StringProperty(0)
    map = ObjectProperty(None)

    def loadFirstMenuPopup(self):
        popup = FirstMenuPopup()
        popup.root = self
        popup.open()
        popup.bind(on_dismiss=self.init_game)

    def server_setup(self):
        # server
        server_lock = Lock()
        server = VttServer('Data/game', server_lock)
        #mainWidget.server_lock = server_lock
        t = Thread(target=server.run)
        t.start()

    def init_game(self, name):
        self.queue = queue.Queue()
        if self.role == 'server' :
            self.server = GMServer(self.queue)
        elif self.role == 'client':
            self.server = ClientConnection(self.queue)

        # map initialization
        self.gameSpace.load_map("Images/map_42x22.png")
        self.gameSpace.load_token("Images/Token_Red_1.png")
        #self.add_widget(self.gameSpace) #necessary ?
        print("game loaded")

    def update(self, dt): #dt as delta time ?
        pass





class VttApp(App):
    def build(self):
        self.mainWidget = MainWidget()
        self.mainWidget.loadFirstMenuPopup()

        Clock.schedule_interval(self.mainWidget.update, 1.0 / 60.0)

        return self.mainWidget


if __name__ == '__main__':
    VttApp().run()


