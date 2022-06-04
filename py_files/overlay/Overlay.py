from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ListProperty, ObjectProperty, StringProperty,
    BooleanProperty
)
#import hell to be dealt with later
# from py_files.gameSpace.TokenManager import *
# from py_files.gameSpace.PingManager import *
# from py_files.gameSpace.Map import *

class Overlay(Widget):
    gameData = ObjectProperty()

    def load_bubble(self, path):
        self.bubbleManager.load_bubble(path, 100)
