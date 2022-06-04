from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ListProperty, ObjectProperty, StringProperty,
    BooleanProperty
)
#import hell to be dealt with later
from py_files.overlay.ContextualMenu import ContextualMenu


class Overlay(Widget):
    gameData = ObjectProperty()

    def load_bubble(self, path):
        self.bubbleManager.load_bubble(path, 100)


    def on_touch_down(self, touch):
        """Game related contextual menu instantiation, called when player right-clicks on the map"""
        # ContextualMenu
        if touch.button == "right":
            self.contextualMenu.disabled = False
            self.contextualMenu.pos = touch.pos
        else :
            self.contextualMenu.disabled = True


        # self.contextualMenuManager.clear_widgets()
