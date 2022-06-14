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
from py_files.other.FileChooserPopup import FileChooserPopup
from py_files.other.FirstMenuPopup import FirstMenuPopup
from py_files.other.GMServer import GMServer

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
    gameData = ObjectProperty(GameData())
    map = ObjectProperty(None)

    def loadFirstMenuPopup(self):
        popup = FirstMenuPopup()
        popup.root = self
        popup.open()
        popup.bind(on_dismiss=self.init_game)

    def init_game(self, name):
        # Server initialization
        self.queue_server = queue.Queue()
        self.queue_game = queue.Queue()
        if self.gameData.role == 'server' :
            self.server = GMServer(self.queue_server, self.queue_game)
        elif self.gameData.role == 'client':
            self.server = ClientConnection(self.queue_server, self.queue_game)

        self.queue_server.put('Initialisation')

        # GameData initialization
        self.gameData.load()

        # GameSpace initialization
        self.gameSpace.gameData = self.gameData
        self.gameSpace.load_map(os.path.join(self.gameData.maps_dir, self.gameData.data['map']))
        for token_info in self.gameData.tokens :
            self.gameSpace.load_token(token_info)

        # Overlay initialization
        self.overlay.gameData = self.gameData
        self.overlay.load_bubble(os.path.join(self.gameData.tokens_dir, "Token_Red_1.png"))
        self.overlay.load_bubble(os.path.join(self.gameData.tokens_dir, "Token_Red_1.png"))

        # RightPanel initialization
        self.rightPanel.gameData = self.gameData
        self.rightPanel.load_chats(self.gameData.game_dir)
        self.rightPanel.size_hint = [0.3, 1]

        print("game loaded")

    def update(self, dt): #dt as delta time ?
        while not self.queue_game.empty() :
            work = self.queue_game.get()
            print(f'MainWidget working on : {work}')
            self.queue_game.task_done()

    def on_stop(self) : #not a kivy function
        print('MainWidget on_stop')
        if self.gameData.role == 'client' :
            self.queue_server.put('quit')
            #self.queue_server.join()
        elif self.gameData.role == 'server' :
            self.queue_server.put('msg:Server shutdown')
            self.queue_server.put('quit')
            #self.queue_server.join()

        # GameData save
        self.gameSpace.update_token_info()
        self.gameData.save()
        print('mainWidget.gameData.save() Done')






class VttApp(App):
    def build(self):
        self.mainWidget = MainWidget()
        self.mainWidget.loadFirstMenuPopup()
        self.mainWidget.queue_game = queue.Queue()

        Clock.schedule_interval(self.mainWidget.update, 1.0 / 60.0)

        return self.mainWidget

    def on_start(self):
        pass

    def on_stop(self):
        print('VttApp on_stop')
        self.mainWidget.on_stop()


if __name__ == '__main__':
    VttApp().run()
    pass


