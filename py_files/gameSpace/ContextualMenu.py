from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ColorProperty, ReferenceListProperty
)
from kivy.clock import Clock


class ContextualMenu(Widget):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)



    def start_vote(self):
        """

        :return:
        """
        print("function start_vote ok")
        pass

    def change_map(self):
        """
        """
        print("function change_map ok")
        pass


class ContextualMenuManager(Widget):
    bg_color = ColorProperty()
    sizeWanted = NumericProperty()

    def on_touch_down(self, touch):
        """Game related contextual menu instantiation, called when player right-clicks on the map"""
        menu = ContextualMenu()
        menu.pos = touch.pos
        self.add_widget(menu)

