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

    def on_disabled(self, origin, new_value) :
        if self.disabled :
            self.opacity = 0
        else :
            self.opacity = 1


