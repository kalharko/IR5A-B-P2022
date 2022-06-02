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


import queue


require('2.1.0')

# Include all our classes :
import os
for depth1 in os.scandir('py_files'):
    if depth1.is_file():
        string = f'from py_files.{depth1.name[:-3]} import *'
        try :
            exec (string)
        except:
            print('Import Error :', string)
    elif depth1.name != '__pycache__' :
        for depth2 in os.scandir(depth1):
            if depth2.is_file():
                string = f'from py_files.{depth1.name}.{depth2.name[:-3]} import *'
                try :
                    exec (string)
                except:
                    print('Import Error :', string)


## Include all the kv files
from kivy.lang import Builder
kv_path = "kv_files"
for depth1 in os.scandir(kv_path):
    if depth1.is_file():
        Builder.load_file(os.path.join(kv_path, depth1.name))
    else:
        for depth2 in os.scandir(depth1):
            if depth2.is_file():
                Builder.load_file(os.path.join(kv_path, depth1.name, depth2.name))






class MainWidget(Widget):
    role = StringProperty(0)
    game_path = StringProperty(0)
    map = ObjectProperty(None)

    def loadFirstMenuPopup(self):
        popup = FirstMenuPopup()
        popup.root = self
        popup.open()
        popup.bind(on_dismiss=self.init_game)

    def init_game(self, name):
        self.queue = queue.Queue()
        if self.role == 'server' :
            self.server = GMServer(self.queue)
        elif self.role == 'client':
            self.server = ClientConnection(self.queue)

        # map initialization
        self.gameSpace.load_map(os.path.join(self.game_path, "Maps", "map_42x22.png"))
        self.gameSpace.load_token(os.path.join(self.game_path, "Tokens", "Token_Red_1.png"))

        self.overlay.load_bubble(os.path.join(self.game_path, "Tokens", "Token_Red_1.png"))
        self.overlay.load_bubble(os.path.join(self.game_path, "Tokens", "Token_Red_1.png"))
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
    pass


